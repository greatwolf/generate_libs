#!/usr/bin/python

import os.path
import cppcodebase
import random
from itertools import product

def CreateNinjafile(libs, classes):
    f = open('build.ninja', 'w')
    liblist = tuple('lib_' + str(i) for i in range(libs))
    classlist = tuple('class_' + str(i) for i in range(classes))
    f.write("""#! ninja
# encoding: utf-8

build_dir = build
cxx = g++
ar = ar
cflags = -g -Wall -pedantic -pipe $
    -O0 -D_WIN32_WINNT=0x0501 -I.
ldflags = -L$build_dir -static
libext  = .a

rule cxx
  command = $cxx -MMD -MT $out -MF $out.d $cflags -c $in -o $out
  description = CXX $out
  depfile = $out.d

rule ar
  command = $ar -cq $out $in
  description = AR $out

rule link
  command = $cxx $ldflags -o $out $in $libs
  description = LINK $out

""")
    for libitem in liblist:
      f.write('build $build_dir\\' + libitem + '$libext: ar')
      for i, classitem in enumerate(classlist):
        if i % 5 == 4: f.write(' $\n ')
        f.write(' ' + '$build_dir\\' + libitem + '\\' + classitem + '.o')
      f.write('\n')

    for libitem in liblist:
      for classitem in classlist:
        f.write('build ' + '$build_dir\\' + libitem + '\\' + classitem + '.o: cxx ' 
                + libitem + '\\' + classitem + '.cpp\n')
      f.write('\n')

    f.write("""
build all: phony""") 
    for i, libitem in enumerate(liblist):
        if i % 5 == 4: f.write(' $\n ')
        f.write(' $build_dir\\' + libitem + '$libext')
    f.write("""\n
default all
""")
    f.close()

def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('ninja')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, (lambda x, y : None))
    CreateNinjafile(libs, classes)
    os.chdir('..')
