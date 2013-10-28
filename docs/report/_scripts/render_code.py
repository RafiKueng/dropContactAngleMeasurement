# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 22:01:42 2013

@author: RafiK
"""

import os

import pygments as pyg
from pygments import lexers
from pygments import formatters


inppath = os.path.abspath('../code/src/')
outpath = os.path.abspath('../code')

outstyle = '__style.tex'

# http://pygments.org/docs/formatters/
latexFormat = pyg.formatters.LatexFormatter(
  linenos=True,
  commandprefix='PYG',
  mathescape=True,
  texcomments=True,
  )


for root, dirs, files in os.walk(inppath):
  for fname in files:
    #if fname != 'json_repr_parts.js': continue
    subdir = root[len(inppath)+1:]

    print '> converting:', subdir, fname, 
    with open(os.path.join(root,fname)) as f:
      code = f.readlines()

    n_pages=0
    first=True
    pages = [[],]
    line_start_numbers = [0]
    offset = 0
    for i, line in enumerate(code):
      if '%%pagebreak%%' in line:
        n_pages+=1
        offset = i
        pages.append([])
        line_start_numbers.append(offset+1)
        continue
      if i-offset>=40:
        if first: print '\n',;first=False
        print "Warning: overfull page @%s:%i > automatic page break" % (fname, i)
        n_pages+=1
        pages.append([])
        offset=i
        line_start_numbers.append(offset+1)
      if len(line) > 70:
        if first: print '\n',;first=False
        print "Warning: overfull line @%s:%i" % (fname, i)
      pages[n_pages].append(line)
      
    #for i, page in enumerate(pages):
    #  pages[i] = '\n'.join(page)
  
    lexer = pyg.lexers.get_lexer_for_filename(fname)
    
    for i, page in enumerate(pages):
      pstr = '' if len(pages)==1 else '_%i'%(i+1)
      latexFormat.linenostart = line_start_numbers[i]
      code = ''.join(page)
      name = (subdir+'-' if subdir else '') + fname + pstr + '.tex'
      p=os.path.join(outpath, name)
      with open(p, 'w') as outfile:
        outstr = pyg.highlight(code, lexer, latexFormat, outfile)
      
    print '>', name
    
print "creating stylefile",
with open(os.path.join(outpath, outstyle), 'w') as f:
  f.write(latexFormat.get_style_defs())