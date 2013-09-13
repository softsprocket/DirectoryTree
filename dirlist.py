import sys
import os
from stat import *

class DirListing(object) :
    """ Recursive mapping of directories """

    def __init__(self, topLevel) :
        if not S_ISDIR(os.stat(topLevel).st_mode) : 
            raise Exception(topLevel + ' is not a directory')
        
        self.dirlisting = {}
        self.__readdir(topLevel, self.dirlisting)


    def __readdir(self, name, dirlist) :
        print 'Listing ' + name
        dname = name.split('/')[-1]
        dirlist[dname] = {'type': 'dir'}
        for f in os.listdir(name) :
            fpath = name + '/' + f
            try :
                st = os.stat(fpath)

                if S_ISREG(st.st_mode) :
                    dirlist[dname][f] = {'type':'file'}
                elif S_ISDIR(st.st_mode) :
                    self.__readdir(fpath, dirlist[dname])

            except OSError:
                print  fpath, sys.exc_info()
                pass

    def listing(self) :
        return self.dirlisting

    def getdirs(self, ls = None):
        if ls is None:
            ls = self.dirlisting

        for each in ls:
            if  ls[each]['type'] == 'dir':
                yield each
                self.getdirs(ls[each])



