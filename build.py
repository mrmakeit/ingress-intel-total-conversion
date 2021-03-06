#!/usr/bin/env python

import glob
import time
import re
import io
import to_uri
def readfile(fn):
    with io.open(fn, 'Ur', encoding='utf8') as f:
        return f.read()

def loaderString(var):
    fn = var.group(1)
    if fn.find('.js')>=0:
      fn1=replaceFile(fn)
    else:
      if fn.find('.css')>=0:
        fn1=replaceFile(fn)
      else:
        fn1=readFile(fn)
    return fn1.replace('\n', '\\n').replace('\'', '\\\'')

def loaderRaw(var):
    fn = var.group(1)
    return replaceFile(fn)

def loaderFile(var):
    fn = var.group(1)
    if fn.find('.js')>=0:
      fn1=replaceFile(fn)
    else:
      if fn.find('.css')>=0:
        fn1=replaceFile(fn)
      else:
        fn1=to_uri.img_to_data(fn)
    return fn1

c = '\n\n'.join(map(readfile, glob.glob('code/*')))
n = time.strftime('%Y-%m-%d-%H%M%S')

def replaceFile(var):
  print var
  m = readfile(var)
  m = m.replace('@@BUILDDATE@@', n)
  m = re.sub('@@INCLUDERAW:([0-9a-zA-Z_./-]+)@@', loaderRaw, m)
  m = re.sub('@@INCLUDESTRING:([0-9a-zA-Z_./-]+)@@', loaderString, m)
  m = re.sub('@@INCLUDEURI:([0-9a-zA-Z_./-]+)@@', loaderFile, m)
  return(m)

m = readfile('main.js')

m = m.split('@@INJECTHERE@@')
m.insert(1, c)
m = '\n\n'.join(m)

m = m.replace('@@BUILDDATE@@', n)
m = re.sub('@@INCLUDERAW:([0-9a-zA-Z_./-]+)@@', loaderRaw, m)
m = re.sub('@@INCLUDESTRING:([0-9a-zA-Z_./-]+)@@', loaderString, m)
m = re.sub('@@INCLUDEURI:([0-9a-zA-Z./-]+)@@', loaderFile, m)
with io.open('iitc-debug.user.js', 'w', encoding='utf8') as f:
    f.write(m)

# vim: ai si ts=4 sw=4 sts=4 et
