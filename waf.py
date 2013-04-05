#!/usr/bin/python

import os.path
import cppcodebase
import random

WT = """#! /usr/bin/env python
# encoding: utf-8

VERSION = '0.0.2'
APPNAME = 'build_bench'
top  = '.'
out  = 'out'

def configure(conf):
    conf.load('g++')

def build(bld):
    for i in range(%d):
        filez = ' '.join(['lib_%%d/class_%%d.cpp' %% (i, j) for j in range(%d)])
        bld.stlib(
            source = filez,
            target = 'lib_%%d' %% i,
            includes = '.', # include the top-level
        )
"""

def CreateTopWaffile(libs, classes):
    f = open('wscript', 'w')
    f.write(WT % (libs, classes))
    f.close()

def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('waf')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, (lambda x, y : None))
    CreateTopWaffile(libs, classes)
    os.chdir('..')
