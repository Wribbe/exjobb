#!/usr/bin/env python3

import json
import sys

key_make = lambda tmp: '_'.join(
  ['_cit']+[''.join(filter(str.isalpha, w.strip().lower())) for w in tmp['title'].split(' ')[:5]]
)

def reads(data):
  dic = {}
  tmp = {}
  for line in data:
    line = line.strip()
    if line.startswith('@'):
      if tmp:
        dic[key_make(tmp)] = tmp
        tmp = {}
      ref_type, ref_key = [v.strip().replace('@','') for v in line.split('{')]
      if ref_key.endswith(','):
        ref_key = ref_key[:-1]
      tmp['key'] = ref_key
      tmp['type'] = ref_type
    elif '=' in line:
      key, value = [t.strip() for t in line.split('=',1)]
      key = key.lower()
      value = value[1:-2].strip()
      if key == "keywords":
        value = sorted([v.strip().lower() for v in value.split(',')])
      elif key == "abstract":
        value = [value[a*80:((a+1)*80)] for a in range((int(len(value)/80))+1) ]
      tmp[key] = value

  dic[key_make(tmp)] = tmp
  return json.dumps(dic, indent=2, sort_keys=True)

def read(filename):
  data = open(filename, 'r').readlines()
  return reads(data)

def main(args):

  if not len(args) > 1:
    print(f"[Usage]: {args[0]} BIBFILE [> output.json]")
    return -1

  print(run(args[1]))

if __name__ == "__main__":
  main(sys.argv)
