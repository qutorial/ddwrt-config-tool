#!/usr/bin/env python3

import argparse

def getParser(description):
  parser = argparse.ArgumentParser(description = description)
  parser.add_argument('--verbose', '-v', action='count')
  return parser

def parseArgs(parser):
  args = parser.parse_args()
  return args
