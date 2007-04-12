
import socket
import select
import threading

from locals import *

BUFSIZE = 1024

class NetBase:
    def __init__(self):
        self._event = []
        self.lock = threading.Lock()
        self.ready_lock = threading.Lock()
        self.buffer = ""
        
        self.ready_lock.acquire()
    
    def parse_cmd(self, cmd):
        cmd = self.buffer + cmd
        cmds = cmd.split(';')
        self.buffer = cmds[-1]
        self.dispatch_events(cmds[:-1])
        
        #print self._event
        
        #self.dispatch_event(cmd)
        # FOR TEST
        #if cmd == "newcard":
        #    self.dispatch_event ("newcard")
            
    def dispatch_events(self, events):
        self.lock.acquire()
        self._event.extend(events)
        self.lock.release()
    
    def dispatch_event(self, event):
        self.lock.acquire()
        self._event.append(event)
        self.lock.release()
        
    def get_events(self):
        self.lock.acquire()
        ret = list(self._event)
        self._event = []
        self.lock.release()
        return ret

class NetServer(NetBase):
    def __init__(self):
        NetBase.__init__(self)
        self.servsock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.servsock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsock.bind (("", PORT))
        self.servsock.listen(5)
        
        self.descriptors = [self.servsock]
        self.t = None
        self._stopevent = threading.Event()
        
    def run_thread(self):
        while not self._stopevent.isSet():
            (sread, swrite,sexc) = select.select (self.descriptors, [], [])
            
            for sock in sread:
                if sock == self.servsock:
                    self.accept_new_connection()
                else:
                    try:
                        str = sock.recv (BUFSIZE)
                        
                        if str == '':
                            sock.close()
                            self.descriptors.remove(sock)
                        else:
                            #host, port = sock.getpeername()
                            self.parse_cmd(str)
                    except socket.error:
                        print 'socket.error!'
                        sock.close()
                        self.descriptors.remove(sock)
                        
    def accept_new_connection(self):
        newsock, (remhost, remport) = self.servsock.accept()
        self.descriptors.append (newsock)
        self.ready_lock.release()
        
    def run(self):
        print "Please wait for client to connect."
        self.t = threading.Thread (target=self.run_thread)
        self.t.setDaemon(1)
        self.t.start()
        
    def send(self, event):
        if len(self.descriptors) <= 1:
            #raise "Connection not established."
            pass
        else:
            self.descriptors[1].send(event)
            
    def close(self):
        self._stopevent.set()
        self.t.join()
        self.servsock.close()

class NetClient(NetBase):
    def __init__(self):
        NetBase.__init__(self)
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsock.connect ((SERVER_IP, PORT))
        self.t = None
        self._stopevent = threading.Event()
        
    def run_thread(self):
        while not self._stopevent.isSet():
            (sread, swrite, sexc) = select.select ([self.clientsock], [], [], 1)
            for sock in sread:
                str = sock.recv (BUFSIZE)
                self.parse_cmd (str)
                
    def run(self):
        self.t = threading.Thread (target=self.run_thread)
        self.t.setDaemon(1)
        self.t.start()
        
    def send(self, event):
        self.clientsock.send (event)
        
    def close(self):
        self._stopevent.set()
        self.t.join()
        self.clientsock.close()
                

class NetConn:
    def __init__(self, is_server):
        self.is_server = is_server
        
        if is_server:
            self.conn = NetServer()
        else:
            self.conn = NetClient()
        self.conn.run()
            
    def send_event(self, event):
        self.conn.send (event)
        
    def get_events(self):
        return self.conn.get_events()
    
    def wait_client(self):
        self.conn.ready_lock.acquire()
        
    def close(self):
        self.conn.close()