#!/usr/bin/python
import sys
import os.path
import random

import cppcodebase
import ant
import bam
import boostbuildv2
import jam
import lake
import make
import msbuild
import msvc2003
import nant
import ninja
import rant
import scons
import sweetbuild
import tundra
import waf

# generate_libs.py root 50 100 15 5
HELP_USAGE = """Usage: generate_libs.py root libs classes internal external.
    root     - Root directory where to create libs.
    libs     - Number of libraries (libraries only depend on those with smaller numbers)
    classes  - Number of classes per library
    internal - Number of includes per file referring to that same library
    external - Number of includes per file pointing to other libraries
"""


def main(argv):
    if len(argv) != 6:
        print(HELP_USAGE)
        return
    
    root_dir = argv[1]
    libs = int(argv[2])
    classes = int(argv[3])
    internal_includes = int(argv[4])
    external_includes = int(argv[5])
    
    cppcodebase.SetDir(root_dir)

    ant.CreateCodebase(libs, classes, internal_includes, external_includes)
    bam.CreateCodebase(libs, classes, internal_includes, external_includes)
    boostbuildv2.CreateCodebase(libs, classes, internal_includes, external_includes)
    jam.CreateCodebase(libs, classes, internal_includes, external_includes)
    lake.CreateCodebase(libs, classes, internal_includes, external_includes)
    make.CreateCodebase(libs, classes, internal_includes, external_includes)
    msbuild.CreateCodebase(libs, classes, internal_includes, external_includes)
    msvc2003.CreateCodebase(libs, classes, internal_includes, external_includes)
    nant.CreateCodebase(libs, classes, internal_includes, external_includes)
    ninja.CreateCodebase(libs, classes, internal_includes, external_includes)
    rant.CreateCodebase(libs, classes, internal_includes, external_includes)
    scons.CreateCodebase(libs, classes, internal_includes, external_includes)
    sweetbuild.CreateCodebase(libs, classes, internal_includes, external_includes)
    tundra.CreateCodebase(libs, classes, internal_includes, external_includes)
    waf.CreateCodebase(libs, classes, internal_includes, external_includes)


if __name__ == "__main__":
    main( sys.argv )
