DirectoryTree
==========

python directory tree object

CLASSES
    DirectoryTree
    Node
        Directory
        File
    
    class Directory(Node)
     |  Object representation of a directory
     |  
     |  Methods defined here:
     |  
     |  __getitem__(self, name)
     |  
     |  __init__(self, path, state)
     |  
     |  __iter__(self)
     |  
     |  find(self, pattern, recurse=False, node=None, col=None)
     |      Search the node names for pattern and return a list
     |      containing any matches. If recurse is set to True it seraches
     |      all nodes beneath this in the tree as well
     |  
     |  values(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Node:
     |  
     |  ls(self)
     |      Print output for the node - similiar to 'ls -la'
    
    class DirectoryTree
     |  Tree representation of directory listing
     |  
     |  Methods defined here:
     |  
     |  __init__(self, path)
     |  
     |  walker(self, callback, node=None)
     |      Traverse the tree executing callback(node) at each node
    
    class File(Node)
     |  Object representation of a file
     |  
     |  Methods defined here:
     |  
     |  __init__(self, path, state)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Node:
     |  
     |  ls(self)
     |      Print output for the node - similiar to 'ls -la'
    
    class Node
     |  Parent class for file and directories
     |  
     |  Methods defined here:
     |  
     |  __init__(self, path, state)
     |  
     |  ls(self)
     |      Print output for the node - similiar to 'ls -la'


