# -*- coding: gb2312 -*-

import sys
import socket
from select import select

import _mysql

try:
    from conf import mysql_conf, app_conf
except:
    print "Can't read the configure file: conf.py"
    print "maybe you must copy conf.py.default to conf.py"
    sys.exit(1)

class Db:
    dangerchars = [';','\'']
    def __init__(self):
        self.__db = None

    def __prepare_db(self):
        self.__db = _mysql.connect(**mysql_conf)

    def __free_db(self):
        if self.__db != None:
            self.__db.close()
            self.__db = None

    def auth(self, uid, pwd):
        self.__prepare_db()
        try:
            try:
                self.__db.query('SELECT * from `user` WHERE user_id=\'%s\' AND user_password=\'%s\'' % (uid, pwd))
                r = self.__db.store_result()
                return r.num_rows() > 0L
            except _mysql.ProgrammingError, error:
                print 'DB ERROR: ProgrammingError'
                print error
                return False
            except Error, error:
                print 'DB ERROR: Error'
                print error
                return False
        finally:
            self.__free_db()

    def decklist(self, uid):
        self.__prepare_db()
        try:
            #try:
                self.__db.query('SELECT id, w_name, w_description from `t_decks_name` WHERE w_user_id=\'%s\'' % uid)
                r=self.__db.store_result()
                ret = []
                for i in r.fetch_row():
                    ret.append({
                        'id':int(i[0]),
                        'name':i[1].decode('gb2312').encode('utf-8'),
                        'description':i[2].decode('gb2312').encode('utf-8')
                        })
                return ret
            #except Error, error:
            #    print 'DB ERROR: Error'
            #    print error
            #    return []
        finally:
            self.__free_db()

    def deckcards(self, deck_name, uid):
        self.__prepare_db()
        try:
            #try:
                self.__db.query('SELECT w_card_name,w_card_img,w_card_num,w_back_num from `t_decks_detail` WHERE w_decks_name=\'%s\' AND w_user_id=\'%s\'' % (deck_name, uid))
                r=self.__db.store_result()
                ret=[]
                for i in r.fetch_row(r.num_rows()):
                    if i[2] is None: num = 0
                    else: num = int(i[2])

                    if i[3] is None: back_num = 0
                    else: back_num = int(i[3])

                    ret.append({
                        'name':i[0],
                        'img_url':i[1],
                        'num':num,
                        'back_num':back_num
                        })
                return ret
            #except Error, error:
            #    print 'DB Error: Error'
            #    print error
            #    return []
        finally:
            self.__free_db()


class Room:
    def __init__(self, serv, name, users=[]):
        self.serv = serv
        self.user_list = users
        self.init_commands()
        self.visible = True
        self.name = name

    def init_commands(self):
        self.__commands = {}
        for i in dir(self):
            if i[-7:]=='Handler':
                self.__commands[i[:-7]]=getattr(self,i)

    def process_cmds(self, fn, cmds):
        for cmd in cmds:
            if ' ' in cmd:
                cmd, msg = cmd.split(' ', 1)
            else:
                cmd, msg = cmd.strip(), ''

            if self.__commands.has_key(cmd):
                self.__commands[cmd](fn, msg)
            else:
                print 'ERROR: unknown command %s' % cmd

    def send(self, fn, msg):
        if not msg.endswith(';'): msg += ';'
        self.serv.send(fn, msg)

    def exitHandler(self, fn, msg):
        self.serv.on_exit(fn)

class Hall(Room):
    def __init__(self, serv, users=[]):
        Room.__init__(self, serv, 'Hall', users)
        self.visible = False

    def roomlistHandler(self, fn, msg):
        self.send(fn, 'roomlist %s' % '\n'.join(['%s:%s'%(room.name,len(room.user_list)) for room in self.serv.rooms]))

    def joinHandler(self, fn, msg):
        room_name = msg.strip()
        if self.serv.game_rooms.has_key(room_name):
            gameroom = self.serv.game_rooms[room_name]
            if len(gameroom.user_list) < 2:
                self.serv.on_join_gameroom(fn, gameroom)
                self.send(fn, 'game_room_joined %s' % room_name)
            else:
                self.send(fn, 'game_room_full')
        else:
            self.send(fn, 'game_room_not_found')

class AuthRoom(Room):
    def __init__(self, serv, users=[]):
        Room.__init__(self, serv, 'auth_room', users)
        self.visible = False

    def authHandler(self, fn, msg):
        tokens = msg.split()
        if len(tokens) != 2:
            print 'ERROR: parameter error for authHandler: %s' % msg
            return

        uid,pwd = tokens

        #TODO: check parameters to prevent an injuery attack

        if self.serv.db.auth(uid,pwd):
            self.send(fn, 'auth_success')
            self.serv.on_auth_success(fn,uid)
        else:
            self.send(fn, 'auth_fail')


class GameRoom(Room):
    def __init__(self, serv, name, users=[]):
        Room.__init__(self, serv, name, users)
        self.__obj_id = 0

    def decklistHandler(self, fn, msg):
        uid = self.serv.username(fn)
        l=self.serv.db.decklist(uid)
        self.send(fn, 'decklist %s' % '\n'.join(['%d:%s:%s'%(d['id'],d['name'].replace(':','_'),d['description'].replace(':','_')) for d in l]))

    def deckcardsHandler(self, fn, msg):
        deck_name = msg.strip()
        uid = self.serv.username(fn)

        l=self.serv.db.deckcards(deck_name, uid)

        p_gen = lambda i: '%d:%s:%s' % (
                self.__obj_id,
                i['name'].replace(':','_'),
                i['img_url'].replace(':','_')
                )
        for i in l:
            num = i['num']
            back_num = i['back_num']
            for j in range(num):
                p = p_gen(i)
                self.send(fn, 'deckcard %s' % p)
                self.__obj_id+=1
            for j in range(back_num):
                p = p_gen(i)
                self.send(fn, 'backcard %s' % p)
                self.__obj_id+=1

class Server:
    def __init__(self):
        db = self.db = Db()
        self.rooms = []

        auth_room = self.__auth_room = AuthRoom(self)
        self.rooms.append(auth_room)
        hall = self.__hall = Hall(self)
        self.rooms.append(hall)

        self.game_rooms = {}
        for i in range(10):
            room_name = 'GameRoom%d' % i
            game_room = GameRoom(self,room_name)
            self.game_rooms[room_name] = game_room
            self.rooms.append(game_room)

        self.__locate = {}
        self.__buffer = {}
        self.__socks = {}
        self.__names = {}
    
    def __work(self):
        self.servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsock.bind(('', app_conf['port']))
        self.servsock.listen(5)
        self.descriptors = [self.servsock]
        
        while True:
            (sread, swrite, sexc) = select (self.descriptors, [], [], 2)
            
            for sock in sread:
                if sock == self.servsock:
                    self.__accept()
                else:
                    try:
                        str = sock.recv(app_conf['bufsize'])
                        
                        if str == '':
                            fn = sock.fileno()
                            self.on_exit(fn)
                        else:
                            fn = sock.fileno()
                            cmd = self.__buffer[fn] + str
                            cmds = cmd.strip(' \r\n\t').split(';')
                            self.__buffer[fn] = cmds[-1]
                            self.__dispatch_cmds(fn, cmds[:-1])
                        
                    except socket.error:
                        print 'socket.error!'
                        sock.close()

    def __dispatch_cmds(self, fn, cmds):
        if self.__locate.has_key(fn):
            room = self.__locate[fn]
            room.process_cmds(fn, cmds)
        else:
            print 'ERROR: request to __locate for unknown fn: %s' % fn
                    
    def __accept(self):
        newsock, (remhost, remport) = self.servsock.accept()
        self.descriptors.append(newsock)
        fn = newsock.fileno()
        self.__buffer[fn] = ''
        self.__locate[fn] = self.__auth_room
        self.__socks[fn]  = newsock

        print 'new sock(fileno: %d) accepted.' % newsock.fileno()
    
    def __cleanup(self):
        for sock in self.descriptors:
            sock.close()

    def on_auth_success(self, fn, uid):
        self.__locate[fn] = self.__hall
        self.__names[fn] = uid

    def on_join_gameroom(self, fn, gameroom):
        self.__locate[fn] = gameroom

    def username(self, fn):
        return self.__names[fn]

    def send(self, fn, msg):
        if self.__socks.has_key(fn):
            self.__socks[fn].send(msg)
        else:
            print 'ERROR: request to __socks with an unknwon key %s in Server.send()' % fn

    def on_exit(self, fn):
        print 'sock(fileno=%d) closed.' % fn
        sock = self.__socks[fn]
        sock.close()
        self.descriptors.remove(sock)
        del self.__socks[fn]
        del self.__locate[fn]
        del self.__buffer[fn]
    
    def start(self):
        print 'Server started. Press ^C to end the program.'
        try:
            self.__work()
        except KeyboardInterrupt:
            self.__cleanup()
            print 'Server end.'


if __name__ == '__main__':
    s = Server()
    s.start()
