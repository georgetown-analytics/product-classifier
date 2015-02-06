# apparel
# Classifier libraries for Apparel
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Feb 05 20:24:45 2015 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Classifier libraries for Apparel
"""

##########################################################################
## Module Methods
##########################################################################

__version__ = (1,0,0)

def get_version():
    """
    Returns a string of the version
    """
    return ".".join(["%i" % i for i in __version__])
