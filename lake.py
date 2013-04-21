#!/usr/bin/python

import os.path
import cppcodebase
import random

LAKE = """--! /usr/bin/env lua
-- For Win32 run as: 
--   lake.lua CC=gcc
--   lake.lua CC=gcc clean
-- encoding: utf-8
local libs    = %d
local classes = %d

local function join(lib_id, numclasses)
    local src_list = {}
    for i = 0, numclasses - 1 do
       src_list[#src_list + 1] = string.format('lib_%%d/class_%%d', lib_id, i)
    end
    return table.concat(src_list, " ")
end

local out = './bin'
lfs.mkdir(out)
local all = {}
lake.set_flags { DEBUG = true }
for i = 0, libs - 1 do
    local lib_i = 'lib_' .. i

    lfs.mkdir(out .. '/' .. lib_i)
    all[#all + 1] =
    cpp.library
    {
        lib_i,
        src = join(i, classes),
        odir = out .. '/' .. lib_i,
        incdir = '.',
        flags = '-O0 -pedantic -pipe'
    }
end

default(all)
"""

def CreateLakefile(libs, classes):
    f = open('lakefile.lua', 'w')
    f.write(LAKE % (libs, classes))
    f.close()

def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('lake')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, (lambda x, y : None))
    CreateLakefile(libs, classes)
    os.chdir('..')
