# -*- coding: gb2312 -*-

from select import select
import socket

PORT = 10021
BUFSIZE = 1024

class Server:
    def __init__(self):
        self.sockhash = {}
        self.peerhash = {}
        self.waitqueue = []
    
    def work(self):
        self.servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsock.bind(('', PORT))
        self.servsock.listen(5)
        self.descriptors = [self.servsock]
        
        while True:
            (sread, swrite, sexc) = select (self.descriptors, [], [], 2)
            
            for sock in sread:
                if sock == self.servsock:
                    self.accept()
                else:
                    try:
                        str = sock.recv(BUFSIZE)
                        
                        if str == '':
                            fn = sock.fileno()
                            print 'sock(fileno=%d) closed.' % fn
                            if sock in self.waitqueue: self.waitqueue.remove(sock)
                            if self.sockhash[fn] == sock: del self.sockhash[fn]
                            if self.peerhash.has_key(fn):
                                peersock = self.peerhash[fn]
                                peersock.send('opponent_leave;')
                                peerfn = peersock.fileno()
                                del self.peerhash[fn]
                                del self.peerhash[peerfn]
                            sock.close()
                            self.descriptors.remove(sock)
                        else:
                            self.send_to_peer(sock, str)
                        
                    except socket.error:
                        print 'socket.error!'
                        sock.close()
                    
    def send_to_peer(self, sock, msg):
        p = self.peer(sock)
        if p is not None:
            p.send(msg)
        
    def peer(self, sock):
        if self.peerhash.has_key(sock.fileno()):
            return self.peerhash[sock.fileno()]
        else:
            return None
        
    def init_sock(self, sock):
        ptr_base = (len(self.descriptors) - 1)*10000
        sock.send('set_obj_ptr %d;' % ptr_base)
        #print 'new ptr_base sent: %d' % ptr_base
        
    def accept(self):
        newsock, (remhost, remport) = self.servsock.accept()
        self.descriptors.append(newsock)
        self.sockhash[newsock.fileno()] = newsock
        
        if len(self.waitqueue) == 0:
            self.waitqueue.append(newsock)
        else:
            waitsock = self.waitqueue.pop()
            self.peerhash[newsock.fileno()] = waitsock
            self.peerhash[waitsock.fileno()] = newsock
            waitsock.send('opponent_found;')
            newsock.send('opponent_found;')
            
        self.init_sock(newsock)
        
        print 'new sock(fileno: %d) accepted.' % newsock.fileno()
    
    def cleanup(self):
        for sock in self.descriptors:
            sock.close()
    
    def start(self):
        print 'Server started. Press ^C to end the program.'
        try:
            self.work()
        except KeyboardInterrupt:
            self.cleanup()
            print 'Server end.'

if __name__ == '__main__':
    s = Server()
    s.start()