#!/usr/bin/python

import os.path
import cppcodebase
import random


def CreateLibMakefile(lib_number, classes):
    os.chdir(cppcodebase.lib_name(lib_number)) 
    handle = open("Makefile", "w");
    handle.write ("""COMPILER = g++
INC = -I..
CCFLAGS = -g -Wall $(INC)
ARCHIVE = ar
.SUFFIXES: .o .cpp

""")
    handle.write ("lib = lib_" + str(lib_number) + ".a\n")
    handle.write ("src = \\\n")
    for i in range(classes):
        handle.write('class_' + str(i) + '.cpp \\\n')
    handle.write ("""
    

objects = $(patsubst %.cpp, %.o, $(src))

all: $(lib)
 
$(lib): $(objects)
	$(ARCHIVE) cr $@ $^

.cpp.o:
	$(COMPILER) $(CCFLAGS) -c $<

clean:
	@del $(objects) $(lib)

""")    
    os.chdir('..')

        
def CreateFullMakefile(libs):
    handle = open("Makefile", "w")

    handle.write('subdirs = \\\n')
    for i in range(libs):
        handle.write('lib_' + str(i) + '\\\n')  
    handle.write("""

all: $(subdirs)
	@for %%i in ($(subdirs)); do \
    $(MAKE) -C %%i all
                
clean:
	@for %%i in ($(subdirs)); do \
	$(MAKE) -C %%i clean
""")
        
def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('make')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, CreateLibMakefile)
    CreateFullMakefile(libs)
    os.chdir('..')
