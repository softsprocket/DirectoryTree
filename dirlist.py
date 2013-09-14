import sys
import os
from stat import *

class Node(object) :
    """ Parent class for file and directories """

    def __init__(self, path, state) :
        self.name = path.split('/')[-1]
        self.path = path
        self.state = state

    
class File(Node) :
    """ Object representation of a file """

    def __init__(self, path, state) :
        Node.__init__(self, path, state)
 
class Directory(Node) :
    """ Object representation of a directory """

    def __init__(self, path, state) :
        Node.__init__(self, path, state)
        
        self.files = {}
        self.directories = {}

        for file in os.listdir(self.path) :
            child = self.path + '/' + file
            
            try :
                st = os.stat(child)

                if S_ISREG(st.st_mode) :
                    self.files[file] = File(child, st)
                elif S_ISDIR(st.st_mode) :
                    self.directories[file] = Directory(child, st)
                else :
                    print 'ignoring ' + child

            except OSError :
                print  child, sys.exc_info()
                pass    


class DirectoryTree(object) :
    """ Tree representation of directory listing """

    def __init__(self, path) :
        state = os.stat(path)

        if not S_ISDIR(state.st_mode) : 
            raise Exception(topLevel + ' is not a directory')
        
        self.root = Directory(path, state)






