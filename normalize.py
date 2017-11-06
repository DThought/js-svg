#!/usr/bin/env python
import re
import sys
import xml.etree.ElementTree as ET


def round_str(n):
  return str(round(n, 3))


def line_to(root, x0, y0, x1, y1, style):
  ET.SubElement(root, 'line', {'x1': round_str(x0), 'y1': round_str(y0), 'x2': round_str(x1), 'y2': round_str(y1), 'style': style})


ns = 'http://www.w3.org/2000/svg'
ET.register_namespace('', ns)
tree = ET.parse(sys.argv[1])
root = tree.getroot()
paths = root.findall('{' + ns + '}path')
modes = 'LMlm'
pair = re.compile(r'([+-]?(\d*\.)?\d+)\s*[\s,]\s*([+-]?(\d*\.)?\d+)')
wsp = re.compile(r'\s+')
for node in root:
  print(node.tag)
for path in paths:
  d = path.get('d')
  i = 0
  x = 0
  y = 0
  mode = None
  while i < len(d):
    if d[i] in modes:
      mode = d[i]
      i += 1
      continue
    if d[i] == 'Z' or d[i] == 'z':
      line_to(root, x, y, x0, y0, path.get('style'))
      x = x0
      y = y0
      i += 1
      continue
    match = pair.match(d[i:])
    if match:
      x1 = float(match.group(1))
      y1 = float(match.group(3))
      if mode == 'l' or mode == 'm':
        x1 += x
        y1 += y
      if mode == 'L' or mode == 'l':
        line_to(root, x, y, x1, y1, path.get('style'))
      elif mode == 'M' or mode == 'm':
        x0 = x1
        y0 = y1
        mode = chr(ord(mode) - 1)
      x = x1
      y = y1
      i += len(match.group())
      continue
    match = wsp.match(d[i:])
    if match:
      i += len(match.group())
      continue
    raise NotImplementedError(d)
  root.remove(path)
tree.write(sys.argv[1], 'UTF-8', True)
