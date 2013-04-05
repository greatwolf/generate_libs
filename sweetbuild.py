#!/usr/bin/python

import os.path
import cppcodebase
import random


def CreateLibBuildfile(lib_number, classes):
    os.chdir(cppcodebase.lib_name(lib_number)) 
    handle = open(cppcodebase.lib_name(lib_number) + ".build", "w");
    handle.write ('Library {\n')
    handle.write ('  id = "' + cppcodebase.lib_name(lib_number) + '";\n');
    handle.write('  Source {\n');

    for i in range(classes):
        handle.write('    "class_' + str(i) + '.cpp",\n')

    handle.write("""  };
}
""")
    os.chdir('..')

        
def CreateFullBuildfile(libs):
    handle = open("build.lua", "w")

    handle.write("""
platform = 'mingw'
variant = 'shipping'
jobs = 1
mingw_directory = "G:/MinGW32-4.6.3"

package.path = root('G:/sweet_build_tool/lua/?.lua') .. ";" .. root('G:/sweet_build_tool/lua/?/init.lua;')
require 'build'
require 'build/mingw'

function initialize()
    local settings = build.initialize {}
    settings.bin = root('.') .. '/bin'
    settings.lib = root('.') .. '/lib'
    settings.include_directories = { root('.') }
    settings.mingw = { mingw_directory = mingw_directory }
    mingw.initialize(settings)
end

function buildfiles()
""")
    for i in range(libs):
        lib_i = 'lib_' + str(i)
        handle.write('    buildfile "' + lib_i + '/' + lib_i + '.build"\n')

    handle.write('end')

def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('sweetbuild')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, CreateLibBuildfile)
    CreateFullBuildfile(libs)
    os.chdir('..')
