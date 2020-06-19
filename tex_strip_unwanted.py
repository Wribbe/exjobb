#!/usr/bin/env python

import sys

def main(args):
  file = args[0]
  lines = open(file, 'r').readlines()
  out = []
  for line in lines:
    if r'\vspace' in line:
      continue
    if r'\newpage' in line:
      continue
    if r'\hspace' in line:
      continue
    out.append(line)
  with open(file, 'w') as fh:
    fh.write(''.join(out)+'\n')


if __name__ == "__main__":
  args = sys.argv[1:]
  main(args)
