"""Constant definition for all the module"""

import os

# directory of vim_pck package
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

# name of the top level section
SECT_1 = "SETTING"
SECT_2 = "REPOSITORY"

# user constant (i.e. variable that the user can change in vimpckrc
# configuration file
PKG_NAME = "package"
TYPE_NAME = "type"
FRZ_NAME = "freeze"

# spinner.py constant
INTERVAL = 0.10
SEQUENCE = "LOSANGE"
OFFSET = 1

# ansi.py constant
LHS = "<"
RHS = ">"
