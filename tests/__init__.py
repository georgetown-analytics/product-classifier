# tests
# Tests for the Apparel package
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 23 08:56:12 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Tests for the Apparel package
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Initialization Test Case
##########################################################################

class InitializationTests(unittest.TestCase):

    def test_initialization(self):
        """
        Assert the world is sane by checking a fact, 2+2=4
        """
        self.assertTrue(2+2, 4)

    def test_import(self):
        """
        We're able to import the apparel library
        """
        try:
            import apparel
        except ImportError:
            self.fail("Was unable to import the Apparel library!")
