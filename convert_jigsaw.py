#!/usr/bin/env python

import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('mesh_file', help='the name of the JIGSAW mesh file')
args = parser.parse_args()

comment = r'^\s*#'
point = r'^POINT'
tri = r'^TRIA'

with open(args.mesh_file) as msh:
    listing = False
    i = 0
    n = 1
    for line in msh:
        if not listing or i >= n:
            if i > n:
                i = 0
                listing = False
                outfile.close()
            if re.search(point, line):
                words = line.split('=')
                i = 0
                n = int(words[1])
                listing = True
                outfile = open('SaveVertices','w')
            elif re.search(tri, line):
                words = line.split('=')
                i = 0
                n = int(words[1])
                listing = True
                outfile = open('SaveTriangles','w')
        else:
            vals = line.split(';')
            outfile.write(f'{vals[0]} {vals[1]} {vals[2]}\n')
            i = i + 1
