"""This module is where the main function for the subcommand of vimpck are
stored
"""

import click
import configparser
import os
from sh import git
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
    if kwargs['config']:
        # click.echo('Configuration file path: %s' % kwargs['config'])
        config.read(kwargs['config'])
    else:
        click.echo('loading the real configuration file')
        config.read([os.path.join(os.environ['XDG_CONFIG_HOME'],
                    'vimpack/config'),
                     os.expanduser('~/.config/vimpck/config')])

    # get all plugin section
    pack_path = config['DEFAULT']['pack_path']
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
    # installed_plug = []
    # for dirpath, dirnames, filenames in utils.walklevel(pack_path, level=3):
    #     installed_plug.append(dirpath)
    installed_plug = utils.instplug(pack_path)

    # filter config entries to only get non-installed plugins
    plug_urls = [sect for sect in plug_urls if not any(config[sect]['plug_locrepo'] in s for s in installed_plug)]

    # install plugins
    for plug_url in tqdm(plug_urls):
        plug_name = os.path.basename(urlparse(plug_url).path)
        plug_locrepo = config[plug_url]['plug_locrepo']
        try:
            output = git.clone(plug_url, plug_locrepo)
        except ErrorReturnCode:
            message = "exit code: %s --> %s" % (str(output), plug_name)
        else:
            message = "Done cloning: %s --> %s" % \
                      (plug_name, os.path.split(plug_locrepo)[0])
        finally:
            tqdm.write(message)

# TODO: Gérer le cas ou le réseau planterait pour la command git clone. Voir
# quel sont les types d'exception géré par sh ?
# TODO: logging
# TODO: pour déclencher l'erreur sur git clone mettre /start à la place de
# start dans le fichier de configuration.
# Faire un test ou je rajoute une entrée dans le fichier de configuration et je
# vois si ce qui se passe avec git clone. Ça va bugger car je ne tiens pas
# compte de cela.
# TODO: Que se passe t'il s'il manque la valeur d'une clé 'key ='
