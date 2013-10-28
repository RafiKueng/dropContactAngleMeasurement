# -*- coding: utf-8 -*-
"""
renders all sequence diagrams

there is some bug in sdedit.. convert to eps or pdf doesn't
work from command line, please do it by hand..

Created on Thu Sep 12 14:50:31 2013

@author: RafiK
"""

import os, time
import subprocess as sp

inppath = os.path.abspath('../seq/src/')
outpath = os.path.abspath('../seq')
#inppath = r'..\seq\src'
#outpath = r'..\seq'


exe_path = r'D:/devtools/sequenzdiagram/'
#exe_path = r'.'
exe_cmd = 'sdedit-4.01.exe'
exe_args = '-t pdf -f A4 -r Landscape --threaded=false' # doesn't work

# there is also linux/max (java) version..
#exe_cmd = 'java -jar sdedit-4.01.jar'
#exe_cmd = 'sdedit.sh'


exep = os.path.join(os.path.abspath(exe_path), exe_cmd)
#args = ' -o %(out)s ' + exe_args + ' %(inp)s'
args = ' --threaded=false -o %(out)s %(inp)s'

def cmd(inp, out):
#  sp.call('pwd')
#  sp.call([exep, args % {'inp':inp, 'out':out}], shell=True)
#  print exep + ' ' + args % {'inp':inp, 'out':out}
  sp.call(exep + ' ' + args % {'inp':inp, 'out':out})
  


if False:
  for root, dirs, files in os.walk(inppath):
    for fname in files:
      print root, dirs, fname
      if fname.endswith('.sdx') or fname.endswith('.sd'):
        name, ext = os.path.splitext(fname)
        tmpname = name + '.eps'
        outname = name + '.pdf'
        inpf = os.path.join(inppath, fname)
        tmpf = os.path.join(outpath, tmpname)
        outf = os.path.join(outpath, outname)
        #inpf = inppath +'\\'+ fname
        #outf = outpath +'\\'+ outname
        print '> convert:', fname
        print inpf
        print tmpf
        print outf
        cmd(inpf, tmpf)
        #sp.call('epstopdf %s' % tmpf)
        
        print '>>', outname, ' STARTED'

#time.sleep(5)      
for fname in os.listdir(outpath):
  if fname.endswith('.eps'):
    e2pc = 'epstopdf %s' % os.path.join(outpath, fname)
    print e2pc
    sp.call(e2pc)