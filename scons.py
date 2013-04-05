#!/usr/bin/python

import os.path
import cppcodebase
import random


def CreateSConscript(lib_number, classes):
    os.chdir(cppcodebase.lib_name(lib_number)) 
    handle = open("SConscript", "w");
    handle.write("Import('env')\n")
    handle.write('list = Split("""\n');
    for i in range(classes):
        handle.write('    class_' + str(i) + '.cpp\n')
    handle.write('    """)\n\n')
    handle.write('env.StaticLibrary("lib_' + str(lib_number) + '", list)\n\n')
    os.chdir('..') 

        
def CreateSConstruct(libs):
    handle = open("SConstruct", "w"); 
    handle.write("""import os\n
env = Environment(tools=['mingw'], CPPFLAGS=['-g', '-O0', '-Wall', '-pedantic', '-pipe'], ENV=os.environ, CPPPATH=[Dir('#')])\n""")
    
    for i in range(libs):
        handle.write("""env.SConscript("lib_%s/SConscript", exports=['env'])\n""" % str(i))  
    
def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('scons')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, CreateSConscript)
    CreateSConstruct(libs)
    os.chdir('..')
