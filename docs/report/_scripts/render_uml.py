# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:38:38 2013

@author: RafiK
"""

import os
import subprocess as sp


dia_bin = r'C:\Program Files (x86)\Dia\bin\dia.exe'
epstopdf = 'epstopdf' # was installed with latex in path

args = ' '.join(['-e "%(out)s"', '-t eps', '"%(inp)s"'])

inp_path = '../uml/src'
out_path = '../uml'

inp_path = os.path.normpath(os.path.abspath(inp_path))
out_path = os.path.normpath(os.path.abspath(out_path))

for root, dirs, files in os.walk(inp_path):
  for fname in files:
    if fname.endswith('.dia'):
      name, ext = os.path.splitext(fname)
      i = os.path.join(inp_path,fname)
      o1 = os.path.join(out_path,'tmp',name+'.eps')
      o2 = os.path.join(out_path,name+'.pdf')
      sp.call(dia_bin + ' ' + args%{'out': o1, 'inp': i})
      sp.call(epstopdf + ' --outfile="%s" '%o2 + o1)

      