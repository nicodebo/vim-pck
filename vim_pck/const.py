"""Constant definition for all the module"""

# user constant (i.e. variable that the user can change in vimpckrc
# configuration file
PKG_NAME = "package"
TYPE_NAME = "type"
FRZ_NAME = "freeze"

# default value if user don't specify anything
PACKAGE = "vimpck"
TYPE = "start"
FREEZE = 0  # false

# spinner.py constant
INTERVAL = 0.10
SEQUENCE = "LOSANGE"
OFFSET = 1

# ansi.py constant
LHS = "<"
RHS = ">"

# default xdg standard directories (if xdg env var not set)
XDG_CONF_DEF = "~/.config/vimpck/config"

# environement variable name
XDG_CONF_NAME = "XDG_CONFIG_HOME"
VIMPCK_CONF_NAME = "VIMPCKRC"
