#!/usr/bin/python
#
# deretina.py
# Written by Cory Alder
# designed to be used as a build script from Xcode
# automatically scales all retina graphics (denoted by <filename>@2x.png) to half size
#
# CONFIGURATION
# depending on your preference, set should_overwrite_existing_files.
# script expects images to be located in $SOURCE_ROOT/Assets/
# (change that on line 33)
#
# INSTALLATION
# Place in $SOURCE_ROOT, and add a run-script build step
# Make sure the run script happens before "copy bundle resources"
#
# Script:
# /usr/bin/python $SOURCE_ROOT/deretina.py
#
# (if you know how to run python direct from Xcode, let me know. cory@davander.com)
#
# last updated Sept. 17th 2011

import os
import commands

imagelist = ['.png','.jpg','.gif']
# file extensions to treat as images

should_overwrite_existing_files = False
# overwrite existing, y/n

resource_root = os.path.join(os.environ['SOURCE_ROOT'],"Assets/")
# path of images, relative to source_root

def crawlFiles(dir):
    basedir = dir
    # print "Files in ", dir, ": "
    subdirlist = []
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(basedir,item)):
        	if isRetinaImage(item): deretina(basedir, item)
        else:
        	if shouldCheck(item): subdirlist.append(os.path.join(basedir, item))
    for subdir in subdirlist:
        crawlFiles(subdir)
        
def isRetinaImage(filename): # check that it's an image and tagged as retina
    basename, extension = os.path.splitext(filename)
    if not basename.endswith('@2x'): return False
    if extension in imagelist: return True
    return False
        
def shouldCheck(dirname): # check that a dir should be searched
    basename, extension = os.path.splitext(dirname)
    if basename.startswith('.'): return False
    if extension == '.xcodeproj': return False
    if basename == 'build' and extension == '': return False
    return True
    
def deretina(dir,file): # 
    filepath = os.path.join(dir,file)
    iWidth = imageWidth(filepath)
    iHeight = imageHeight(filepath)
    outWidth, outHeight = canDeretina(iWidth,iHeight)
    if not outWidth or not outHeight:
        print "Can't deretina "+filepath+' ('+iWidth+', '+iHeight+')'
        return
    else:
        unretFilename = file.replace('@2x','')
        if not os.path.exists(os.path.join(dir,unretFilename)) or should_overwrite_existing_files == True:
            print "Deretina-ing "+filepath+' ('+iWidth+', '+iHeight+')'
            doCmd = 'sips -z {} {} {} --out {}'.format( outHeight, outWidth, commands.mk2arg('',filepath), commands.mk2arg(dir,unretFilename ))
            status, output = commands.getstatusoutput(doCmd)
        else:
            print "Already deretina-ed "+filepath+' ('+iWidth+', '+iHeight+')'

def canDeretina(height,width):
    try:
        hn = int(height.strip().split()[0])
        wn = int(width.strip().split()[0])
    except (ValueError, IndexError):
        return None, None
    return hn/2, wn/2

def imageWidth(filepath):
    return getProperty(filepath, 'pixelWidth')
    
def imageHeight(filepath):
    return getProperty(filepath, 'pixelHeight')
    
def getProperty(filepath, property):
    status, output = commands.getstatusoutput('sips -g '+property+' '+commands.mk2arg('',filepath))
    outputlist = output.split(property+': ')
    prop = outputlist.pop()
    return prop

crawlFiles(resource_root)