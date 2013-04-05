#!/usr/bin/python

import os.path
import cppcodebase
import random

BAM = """--! /usr/bin/env lua
-- encoding: utf-8

settings = NewSettings()
SetDriversGCC(settings)
local function buildDir(settings, input)
    return ".bam\\\\" .. PathBase(input)
end

settings.cc.Output = buildDir
settings.lib.Output = buildDir
settings.cc.flags:Add('-pedantic', '-Wall', '-O0', '-pipe')
settings.cc.includes:Add('.')
for i = 0, %d - 1 do
  local src = Collect(string.format("lib_%%d/*.cpp", i))
  local obj = Compile(settings, src)
  local lib = StaticLibrary(settings, "_" .. i, obj)
end
"""

def CreateBamfile(libs, classes):
    f = open('bam.lua', 'w')
    f.write(BAM % libs)
    f.close()

def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('bam')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, (lambda x, y : None))
    CreateBamfile(libs, classes)
    os.chdir('..')
