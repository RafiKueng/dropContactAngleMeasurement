# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:30:57 2013

@author: RafiK
"""

import os
import subprocess as sp

lo = r'C:\Program Files (x86)\LibreOffice 4\program\soffice.exe'

args = ' '.join(['--headless', '--convert-to pdf', '--outdir "%(out)s"', '"%(inp)s"'])

inp_path = '../fig/src'
out_path = '../fig'

inp_path = os.path.normpath(os.path.abspath(inp_path))
out_path = os.path.normpath(os.path.abspath(out_path))

for root, dirs, files in os.walk(inp_path):
  for fname in files:
    if fname.endswith('.odg'):
      i = os.path.join(inp_path,fname)
      sp.call(lo + ' ' + args%{'out': out_path, 'inp': i})
      
