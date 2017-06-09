"""This module is where the main function for the subcommand of vimpck are
stored
"""

import os
import subprocess
import sys
from tqdm import tqdm
from urllib.parse import urlparse

from vim_pck import utils
from vim_pck import spinner
from vim_pck import git


def install_cmd():
    """Install function. This function is launched when the ``vimpck install``
    command is invoked.
    """

    vimpckrc = utils.ConfigFile()
    plugfilt = utils.UrlFilter()

    try:
        os.makedirs(vimpckrc.pack_path)
    except OSError:
        pass

    pluglist = utils.PluginList(vimpckrc.pack_path)
    vimpckrc.getplugurls()
    vimpckrc.tagplugentries()

    plugfilt.install(vimpckrc.valid_plug_entries, pluglist.installed_plug.keys())

    if not plugfilt.toinstall_plug:
        print('no plugin to install !')
    else:
        print(':: Installing plugins...')
        for remote_url in plugfilt.toinstall_plug:
            info = "{}".format(remote_url)
            seq = 'LOSANGE'
            interval = 0.15
            offset = 1
            a_spinner = spinner.Spinner(info, interval, seq, offset)
            local_dir = os.path.join(vimpckrc.pack_path,
                                     vimpckrc.config[remote_url]['package'],
                                     vimpckrc.config[remote_url]['type'])
            try:
                os.makedirs(local_dir)
            except OSError:
                pass
            #TODO: make a wrapper function for directory creation or integrate
            # it into the git.Clone class
            tmp_cloner = git.Clone(remote_url, local_dir)
            a_spinner.start()
            out = tmp_cloner.git_cmd()
            a_spinner.stop()
            if out == 0:
                print("{}: \u001b[32mDone ✓\u001b[0m".format(info))
            else:
                print("{}: \u001b[31mFail ✗\u001b[0m".format(info))
                print("  {}".format(tmp_cloner.error_proc.stderr))
            del a_spinner
            del tmp_cloner
            #TODO: Make some helper function that enclose some string into ANSI
            # escape sequence
            #TODO: Add an offset parameter for the spinner message
            #TODO: Make a wrapper function that add x number of space before
            # some string


def ls_cmd(**kwargs):
    """list function. This function is launched when the ``vimpck ls``
    command is invoked.

    Arg:
        **kwarg (str) : an argument is present, kwargs['start']/kwarg['opt'] to
        filter autostart/optional plugins
    """

    vimpckrc = utils.ConfigFile()
    if not os.path.isdir(vimpckrc.pack_path):
        sys.exit("{} does not exist. Use vimpck install".format(vimpckrc.pack_path))

    plugls = utils.PluginList(vimpckrc.pack_path)

    if kwargs['start']:
        plugls.autostart()
        plug = plugls.start_plug
    elif kwargs['opt']:
        plugls.optional()
        plug = plugls.opt_plug
    else:
        plug = []
        for key in plugls.installed_plug.keys():
            plug.append(key)

    return plug


def upgrade_cmd(**kwargs):
    """Upgrade function. This function is launched when the ``vimpck upgrade``
    command is invoked.
    """

    vimpckrc = utils.ConfigFile()
    vimpckrc.getplugurls()
    vimpckrc.tagplugentries()
    vimpckrc.nonfreezedurl()
    plugfilt = utils.UrlFilter()

    try:
        plug = kwargs['plug']
    except KeyError:
        plug = []

    plugfilt.upgrade(vimpckrc.nonfreeze_urls, vimpckrc.pack_path, plug)

    giterror = []
    current_sha = ""
    new_sha = ""
    git_commit_range = []  # store plugin name, current and last commit
    for plug_url in tqdm(plugfilt.toupgrade_plug):
        temperror = []
        plug_name = os.path.basename(urlparse(plug_url).path)
        plug_locrepo = os.path.join(vimpckrc.pack_path,
                                    vimpckrc.config[plug_url]['package'],
                                    vimpckrc.config[plug_url]['type'],
                                    plug_name)

        a = subprocess.run(["git", "-C", plug_locrepo, "rev-list", "-1", "HEAD"],
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           check=True)
        current_sha = a.stdout.decode('UTF-8').rstrip()
        new_sha = ""
        del a

        try:
            subprocess.run(["git", "-C", plug_locrepo, "pull"],
                           stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            message = "Failed pulling : exit code: %s --> %s" % \
                      (e.returncode, plug_name)
            temperror.append(plug_name)
            temperror.append(plug_url)
            temperror.append(e.returncode)
            temperror.append(e.cmd)
            temperror.append(e.stderr)
            giterror.append(temperror)
        else:
            message = "Done updating: %s --> %s" % \
                      (plug_name, plug_locrepo)

            b = subprocess.run(["git", "-C", plug_locrepo,
                               "rev-list", "-1", "HEAD"],
                               stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                               check=True)
            new_sha = b.stdout.decode('UTF-8').rstrip()
            del b
            git_commit_range.append([plug_name, plug_locrepo,
                                    current_sha, new_sha])
        finally:
            tqdm.write(message)

    if giterror:
        for err in giterror:
            message = "\n--> plug name: {0} \nplug url: {1} \ncmd: {2} \nerror code: {3} \nerror message: {4} \n".format(err[0], err[1], " ".join(err[3]), err[2], err[4].decode('UTF-8'))
            print(message)

    if git_commit_range:
        for elem in git_commit_range:
            if elem[2] == elem[3]:
                print("\n plug name: {} --> already up to date\n".format(elem[0]))
            else:
                print("\nplug name: {}".format(elem[0]))
                c = subprocess.run(["git", "--no-pager", "-C", elem[1], "log", "--graph", "--oneline", "--decorate", "{0}..{1}".format(elem[2], elem[3])], stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
                print(c.stdout.decode('UTF-8'))
