import sys
import os
from stat import *
import pwd
import grp
import time
import re

class Node :
    """ Parent class for file and directories """

    def __init__(self, path, state) :
        self.name = path.split('/')[-1]
        self.path = path
        self.state = state

    def ls(self) :
        """ Print output for the node - similiar to 'ls -la' """

        print '%s %d %s %s %d %s %s' % (self.__lsmodes(self.state.st_mode), 
                                self.state.st_nlink, 
                                pwd.getpwuid(self.state.st_uid).pw_name, 
                                grp.getgrgid(self.state.st_gid).gr_name,
                                self.state.st_size,
                                self.__maketime(time.localtime(self.state.st_mtime)),
                                self.name)


    def __maketime(self, tm) :
        t = '%b %d '
        now = time.localtime()
        if tm.tm_year != now.tm_year :
            t += '%Y '

        t += '%H:%M:%S'

        return time.strftime(t, tm)

        

    def __lsmodes(self, mode) :
        ba = bytearray(' ' * 10)

        ifmt = S_IFMT(mode)
        
        if S_ISDIR(ifmt) :
            ba[0] = ord('d')
        elif S_ISCHR(ifmt) :
            ba[0] = ord('c')
        elif S_ISBLK(ifmt) :
            ba[0] = ord('b')
        elif S_ISLNK(ifmt) :
            ba[0] = ord('l')
        elif S_ISSOCK(ifmt) :
            ba[0] = ord('s')
        elif S_ISFIFO(ifmt) :
            ba[0] = ord('p')
        else :
            ba[0] = ord('-')

        self.__rwx(ba, 1, mode)
        self.__rwx(ba, 4, mode << 3)
        self.__rwx(ba, 7, mode << 6)

        if (mode & S_ISUID) :
            ba[3] = ord('s') if (mode & S_IEXEC) else ord('S')

        if (mode & S_ISGID) :
            ba[6] = ord('s') if (mode & (S_IEXEC >> 3)) else ord('S')

        if (mode & S_ISVTX) :
            ba[9] = ord('t') if (mode & (S_IEXEC >> 6)) else ord('T')

        return ba


    def __rwx(self, ba, pos, mode) :

        if (mode & S_IREAD) :
            ba[pos] = ord('r')
        else :
            ba[pos] = ord('-')

        if (mode & S_IWRITE) :
            ba[pos + 1] = ord('w')
        else :
            ba[pos + 1] = ord('-')

        if (mode & S_IEXEC) :
            ba[pos + 2] = ord('x')
        else :
            ba[pos + 2] = ord('-')

       

    
class File(Node) :
    """ Object representation of a file """

    def __init__(self, path, state) :
        Node.__init__(self, path, state)
 
class Directory(Node) :
    """ Object representation of a directory """

    def __init__(self, path, state) :
        Node.__init__(self, path, state)
        
        self.nodes = {}

        for file in os.listdir(self.path) :
            child = self.path + '/' + file
            
            try :
                st = os.stat(child)

                if S_ISREG(st.st_mode) :
                    self.nodes[file] = File(child, st)
                elif S_ISDIR(st.st_mode) :
                    self.nodes[file] = Directory(child, st)
                else :
                    print 'ignoring ' + child

            except OSError :
                print  child, sys.exc_info()
                pass    

    def __getitem__(self, name) :
        return self.nodes[name]

    def __iter__(self) :
        return iter(self.nodes)

    def values(self) :
        return self.node.values()

    def find(self, pattern, recurse = False, node = None, col = None) :
        """ Search the node names for pattern and return a list
            containing any matches. If recurse is set to True it seraches
            all nodes beneath this in the tree as well
        """
        
        if node is None :
            node = self.nodes

        if col is None :
            col = []

        for n in node :
            if re.search(pattern, n) is not None :
                col.append(node[n])
    
            if isinstance(node[n], Directory) :
                self.find(pattern, recurse, node[n], col)

        return col               
                
            
class DirectoryTree :
    """ Tree representation of directory listing """

    def __init__(self, path) :
        state = os.stat(path)

        if not S_ISDIR(state.st_mode) : 
            raise Exception(topLevel + ' is not a directory')
        
        self.root = Directory(path, state)


    def walker (self, callback, node = None) :
        """ Traverse the tree executing callback(node) at each node """

        if node == None :
            node = self.root
        
        for n in node :
            callback(node[n])
            if isinstance(node[n], Directory) :
                self.walker(callback, node[n])

