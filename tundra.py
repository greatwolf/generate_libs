#!/usr/bin/python

import os.path
import cppcodebase
import random

TUNDRAUNITS = """--! /usr/bin/env lua
-- encoding: utf-8

for i = 0, %d - 1 do
    local libname = string.format("lib_%%d", i)
    local src = {}
    for j = 0, %d - 1 do
      src[#src + 1] = string.format("lib_%%d/class_%%d.cpp", i, j)
    end
    
    StaticLibrary
    {
        Name = libname,
        Sources = src,
        Env = 
        {
            CPPPATH = '.'
        }
    }
    Always(libname)
end
"""

TUNDRA = """--! /usr/bin/env lua
-- encoding: utf-8
VERSION = '0.0.2'
APPNAME = 'build_bench'
top  = '.'
out  = 'tbuild'

local common = 
{
	Env = {
		CXXOPTS = {
			{ "-pedantic", "-Wall", "-Werror"; Config = "*-mingw-*" },
			{ "-g"; Config = "*-mingw-debug" },
			{ "-O2"; Config = { "*-mingw-release", "*-bcc-release" } },
			{ "-v"; Config = "*-bcc-debug" },
			{ "-WMC"; Config = "*-bcc-*" },
		},
		CPPDEFS = {
			{ "NDEBUG"; Config = "*-*-release" },
		},
        LIBS = {
            { "cw32mt.lib", "c0x32.obj"; Config = "*-bcc-*" },
        },
        PROGOPTS = {
            { "-ap", "-Tpe"; Config = "*-bcc-*" },
            { "-v"; Config = "*-bcc-debug"},
        },
	};
	ReplaceEnv = { OBJECTROOT = out, }
}

Build 
{
	Units = "units.lua",
	SyntaxExtensions = { "tundra.syntax.glob", "tundra.syntax.embed_lua" },
	Configs = {
		Config { Name = "win32-mingw", Inherit = common, Tools = { "mingw" } },
		Config { Name = "win32-bcc", Inherit = common, Tools = { "bcc" } },
		Config { Name = "win32-winsdk7", Inherit = common, Tools = { "msvc-winsdk"; TargetArch = "x86", VcVersion = "10.0" } },
	},
}
"""

def CreateTundrafiles(libs, classes):
    f = open('units.lua', 'w')
    f.write(TUNDRAUNITS % (libs, classes))
    f.close()
    
    f = open('tundra.lua', 'w')
    f.write(TUNDRA)
    f.close()

def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('tundra')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, (lambda x, y : None))
    CreateTundrafiles(libs, classes)
    os.chdir('..')
