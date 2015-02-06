# apparel.config
# Uses confire to get meaningful configurations from a yaml file
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Sep 19 11:14:33 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: config.py [] benjamin@bengfort.com $

"""
Uses confire to get meaningful configurations from a yaml file
"""

##########################################################################
## Imports
##########################################################################

import os
import confire

##########################################################################
## Configuration
##########################################################################

class ApparelConfiguration(confire.Configuration):
    """
    Meaningful defaults and required configurations.

    debug:    the app will print or log debug statements
    testing:  the app will not overwrite important resources
    corpus:   the location of the corpus on disk
    model:    the location of the pickled model on disk
    """

    CONF_PATHS = [
        "/etc/apparel.yaml",                     # System configuration
        os.path.expanduser("~/.apparel.yaml"),   # User specific config
        os.path.abspath("conf/apparel.yaml"),    # Local configuration
    ]

    debug    = True
    testing  = True
    corpus   = None
    model    = None


## Load settings immediately for import
settings = ApparelConfiguration.load()

if __name__ == '__main__':
    print settings
