# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 18:39:46 2012

@author: rafik
"""

import os
import inspect
import plugins.helper as h

plugin_dir = 'plugins'
plugin_dir_base = '.'

def get_plugin_tree():
    module_list = []
    for file in os.listdir(plugin_dir_base+'/'+plugin_dir):
        mod_name, mod_ext = os.path.splitext(file)
        if (mod_ext in ['.py', '.pyc', '.pyo']
            and not mod_name in ['Abstract', 'helper', '__init__']
            and not mod_name in module_list):
            module_list.append(mod_name)
    
    module_list = set(module_list) #remove dublicates
    
    #print module_list
    
    tree = []
    flatlist = []
    
    for mod_name in module_list:
        module = __import__(plugin_dir+'.'+mod_name, fromlist=plugin_dir)
        classes_of_module = []
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj)
                and issubclass(obj, h.AbstractPlugin)
                and hasattr(obj, '__type__')):
    #            print name
    #            print '   ',obj
    #            print '   ',issubclass(obj, h.AbstractPlugin), inspect.isclass(obj)
    #            print '   ',getattr(obj, '__doc__') 
                #for i in inspect.getmembers(obj): print i
                classes_of_module.append((  name,
                                            obj,
                                            getattr(obj, '__type__'),
                                            getattr(obj, '__doc__')))
                flatlist.append((mod_name,
                                 module.__doc__,
                                 name,
                                 obj,
                                 getattr(obj, '__type__'),
                                 getattr(obj, '__doc__')))

        if len(classes_of_module)>0:
            tree.append([mod_name, module.__doc__, classes_of_module])
    
    return tree
    #return flatlist
    
'''
datastructre of tree:
    list with [module_name, module_docsting, list_of_classes]
    
    with list_of_classes as a list of available plugins (surprise..):
    [plugin_name, pointer_to_plugin, plugin_type, plugin_docstring]

datastructre of flatlist:
    [module_name, module_docstring, plugin_name, pointer_to_plugin, plugin_type, plugin_docstring]
    contains an entry for each plugin in a module
''' 



def main():
    """this will only be used for debugging..."""
    tree = get_plugin_tree()
    
    for i,k, j in tree:
        print '\n*',i, k
        for jj in j:
            print '  -', jj
            
    return




def init_class():
    pass




if __name__ == '__main__':

    def cmdmain(*args):
        try:
            main()
        except:
            # handle general exceptions
            raise
        else:
            return 0 #exit with errorcode 0 = everything ok

    #sys.exit(cmdmain(*sys.argv))
    cmdmain()
    
else:
    init_class()