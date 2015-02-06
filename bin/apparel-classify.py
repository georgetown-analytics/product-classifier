#!/usr/bin/env python
# apparel-classify
# Command line script to execute classification commands
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  timestamp
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: apparel-classify.py [] benjamin@bengfort.com $

"""
Command line script to execute classification commands.

There are two primary commands:

    - build (builds the model)
    - classify (classifies the input text)

These commands are dependent on configurations found in conf/apparel.yaml
"""

##########################################################################
## Imports
##########################################################################

import os
import sys

## Helper to add apparel to Python Path for development
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import apparel
import argparse

from apparel.config import settings

##########################################################################
## Main method
##########################################################################

if __name__ == '__main__':
    print settings
