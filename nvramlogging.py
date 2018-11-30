#!/usr/bin/env python3
import logging

def getLogger(args):
  logger = logging.getLogger('nvram_tool')
  if args.verbose is None:
    logger.setLevel(logging.ERROR)
  elif args.verbose == 1:
      logger.setLevel(logging.INFO)
  elif args.verbose >= 2:
      logger.setLevel(logging.DEBUG)
  ch = logging.StreamHandler()
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)
  return logger

def getTestLogger():
  logger = logging.getLogger('test')
  logger.setLevel(logging.ERROR)
  return logger

