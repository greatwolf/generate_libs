#!/usr/bin/python

import os.path
import cppcodebase
import random

   
def LibraryGUID(lib_number):
    return 'CF495178-8865-4D20-939D-AAA' + '%07d' % (lib_number)
    
def CreateMSVCXProjFile(lib_number, classes):
    os.chdir(cppcodebase.lib_name(lib_number)) 
    handle = open("lib_" + str(lib_number) + ".vcxproj", "w")
    handle.write("""<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    <ProjectConfiguration Include="Debug|Win32">
      <Configuration>Debug</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|Win32">
      <Configuration>Release</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
  </ItemGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.default.props" />
  <PropertyGroup>
    <ConfigurationType>StaticLibrary</ConfigurationType>
    <ProjectGuid>{ """ + LibraryGUID(lib_number) + """}</ProjectGuid>
    <ShowAllFiles>false</ShowAllFiles>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)/Microsoft.Cpp.props" />
  <ItemDefinitionGroup>
    <ClCompile>
      <Optimization>Disabled</Optimization>
      <AdditionalIncludeDirectories>..;</AdditionalIncludeDirectories>
      <PreprocessorDefinitions>WIN32;_DEBUG;_LIB;</PreprocessorDefinitions>
      <MinimalRebuild>true</MinimalRebuild>
      <WarningLevel>Level3</WarningLevel>
      <DebugInformationFormat>ProgramDatabase</DebugInformationFormat>
    </ClCompile>
  </ItemDefinitionGroup>
  <ItemGroup>
""")
    for i in range(classes):
        handle.write('    <ClCompile Include=".\class_' + str(i) + '.cpp"/>\n')

    handle.write("""
  </ItemGroup>
  <ItemGroup>
""")
    for i in range(classes):
        handle.write('    <ClInclude Include=".\class_' + str(i) + '.h"/>\n')
  
    handle.write("""
  </ItemGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Targets" />
</Project>
""")
    os.chdir('..') 


def CreateMSVCSolution(libs):
    handle = open("solution.sln", "w")
    handle.write("Microsoft Visual Studio Solution File, Format Version 11.00\n")
    
    for i in range(libs):
        project_name = cppcodebase.lib_name(i) + '\\' + cppcodebase.lib_name(i) + '.vcxproj'
        handle.write('Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = "' + cppcodebase.lib_name(i) + 
                      '", "' + project_name + '", "{' + LibraryGUID(i) + '}"\n')
        handle.write('EndProject\n')
    
    handle.write("""
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Win32 = Debug|Win32
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
""")
    for i in range(libs):
        handle.write("""		{""" + LibraryGUID(i) + """}.Debug|Win32.ActiveCfg = Debug|Win32
		{""" + LibraryGUID(i) + """}.Debug|Win32.Build.0 = Debug|Win32
""")
    handle.write("""	EndGlobalSection
EndGlobal
""")


def CreateCodebase(libs, classes, internal_includes, external_includes):
    cppcodebase.SetDir('msbuild')
    cppcodebase.CreateSetOfLibraries(libs, classes, internal_includes, external_includes, CreateMSVCXProjFile)
    CreateMSVCSolution(libs)
    os.chdir('..')
