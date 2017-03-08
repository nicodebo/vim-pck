"""This module is where the main function for the subcommand of vimpck are
stored
"""

import configparser
import os
import sys
# from sh import git
import sh
from tqdm import tqdm
from urllib.parse import urlparse

from vim_pck import utils


def install_cmd(**kwargs):
    """Install function. This function is launched when the ``vimpck install``
    command is invoked.

    Only install plugin that are currently not present on the pack directory

    Arg:
        **kwarg (str) : an argument is present, kwargs['config'] only if the
        --congig flag of the install subcommand was specified. It used to
        specify an alternate configuration file. Used for testing purpose.
    """

    config = configparser.ConfigParser()

    try:
        conf_path = os.environ['VIMPCKRC']
    except KeyError:
        conf_path = os.getenv(os.path.join(os.environ['XDG_CONFIG_HOME'],
                                           'vimpck/config'),
                              os.path.expanduser('~/.config/vimpck/config'))
    finally:
        if os.path.exists(conf_path):
            config.read(conf_path)
        else:
            sys.exit("No configuration file found!")

    # get all plugin section
    pack_path = os.path.expanduser(config['DEFAULT']['pack_path'])
    try:
        os.makedirs(pack_path)
    except OSError:
        pass

    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']

    # get valid entries (plug_locrepo != '')
    for plug_url in plug_urls:
        plug_name = os.path.basename(urlparse(plug_url).path)
        try:
            plug_locrepo = os.path.join(pack_path,
                                        config[plug_url]['package'],
                                        config[plug_url]['type'], plug_name)
        except KeyError:
            plug_locrepo = ''
        finally:
            config[plug_url]['plug_locrepo'] = plug_locrepo

    # get already installed plugins
    installed_plug = utils.instplug(pack_path)

    # filter config entries to only get non-installed plugins
    plug_urls_fil = []
    for plug_url in plug_urls:
        if not any(os.path.basename(urlparse(config[plug_url]['plug_locrepo']).path) in s for s in installed_plug):
            plug_urls_fil.append(plug_url)

    # install plugins
    for plug_url in tqdm(plug_urls_fil):
        plug_name = os.path.basename(urlparse(plug_url).path)
        plug_locrepo = config[plug_url]['plug_locrepo']
        try:
            output = sh.git.clone(plug_url, plug_locrepo)
        except sh.ErrorReturnCode_128:
            message = "exit code: %s --> %s" % (str(output), plug_name)
        else:
            message = "Done cloning: %s --> %s" % \
                      (plug_name, os.path.split(plug_locrepo)[0])
        finally:
            tqdm.write(message)

# TODO: pour déclencher l'erreur sur git clone mettre /start à la place de
# start dans le fichier de configuration.
# Faire un test ou je rajoute une entrée dans le fichier de configuration et je
# vois si ce qui se passe avec git clone. Ça va bugger car je ne tiens pas
# compte de cela.
# TODO: exception for git clone doesn't work
