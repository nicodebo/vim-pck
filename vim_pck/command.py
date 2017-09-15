"""This module is where the main function for the subcommand of vimpck are
stored
"""

import os
import sys
import shutil

from vim_pck import utils
from vim_pck import spinner
from vim_pck import git
from vim_pck import ansi
from vim_pck import const


def install_cmd():
    """Install function. This function is launched when the ``vimpck install``
    command is invoked.
    """

    vimpckrc = utils.ConfigFile()
    os.makedirs(vimpckrc.pack_path, exist_ok=True)
    pluglist = utils.DiskPlugin(vimpckrc.pack_path)

    diff = set(vimpckrc.freeze_false()).symmetric_difference(set(pluglist.all_plug.values()))

    if not diff:
        print('no plugin to install !')
    else:
        ansi_tran = ansi.Parser(const.LHS, const.RHS)
        title = "<bold>:: Installing plugins...<reset>"
        print(ansi_tran.sub(title))
        for remote_url in diff:
            info = "{}".format(remote_url)
            a_spinner = spinner.Spinner(info, const.INTERVAL,
                                        const.SEQUENCE, const.OFFSET)
            local_dir = os.path.join(vimpckrc.pack_path,
                                     vimpckrc.config[const.SECT_2][remote_url][const.PKG_NAME],
                                     vimpckrc.config[const.SECT_2][remote_url][const.TYPE_NAME])
            os.makedirs(local_dir, exist_ok=True)
            tmp_cloner = git.Clone(remote_url, local_dir)
            a_spinner.start()
            out = tmp_cloner.git_cmd()
            a_spinner.stop()
            if out == 0:
                status = "✓ {}: <green>Installed<reset>".format(info)
                status = status.rjust(len(status) + const.OFFSET)
                status = ansi_tran.sub(status)
                print(status)
            else:
                status = "✗ {}: <red>Fail<reset>".format(info)
                status = status.rjust(len(status) + const.OFFSET)
                status = ansi_tran.sub(status)
                print(status)
                err_status = tmp_cloner.error_proc.stderr.decode('UTF-8')
                # TODO: duplicate the retrieve_stdout method, merge them
                err_status = err_status.rjust(len(err_status) + const.OFFSET + 2)
                print(err_status)
            del a_spinner
            del tmp_cloner
            # TODO: more beautiful output info, see zplug update, also show the
            # pack path


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

    plugls = utils.DiskPlugin(vimpckrc.pack_path)

    if kwargs['start']:
        plug = plugls.filt_plug('start')
    elif kwargs['opt']:
        plug = plugls.filt_plug('opt')
    else:
        plug = plugls.all_plug.keys()

    return plug
# TODO: display something if pack exists but no plugins inside


def upgrade_cmd(**kwargs):
    """Upgrade function. This function is launched when the ``vimpck upgrade``
    command is invoked.
    """

    vimpckrc = utils.ConfigFile()
    os.makedirs(vimpckrc.pack_path, exist_ok=True)
    pluglist = utils.DiskPlugin(vimpckrc.pack_path)

    plug = {k: v for k, v in pluglist.all_plug.items() if v in vimpckrc.freeze_false()}

    if kwargs['plug']:
        plug = {k: v for k, v in pluglist.all_plug.items() if k in kwargs['plug']}

    if not plug:
        sys.exit('no plugins to be upgraded!')

    ansi_tran = ansi.Parser(const.LHS, const.RHS)
    title = "<bold>:: Upgrading plugins...<reset>"
    print(ansi_tran.sub(title))
    for path in plug.keys():
        info = "{}".format(plug[path])
        a_spinner = spinner.Spinner(info, const.INTERVAL,
                                    const.SEQUENCE, const.OFFSET)
        local_dir = os.path.join(vimpckrc.pack_path, path)

        tmp_puller = git.Pull(local_dir)
        tmp_hasher = [git.Hash(local_dir) for i in range(2)]
        tmp_hasher[0].git_cmd()
        hash_bef = tmp_hasher[0].retrieve_stdout()
        a_spinner.start()
        out = tmp_puller.git_cmd()
        a_spinner.stop()
        tmp_hasher[1].git_cmd()
        hash_aft = tmp_hasher[1].retrieve_stdout()
        if out == 0:
            if hash_bef == hash_aft:
                message = "<yellow>Already up to date<reset>"
            else:
                message = "<green>Updated"
            status = "✓ {}: <green>{}<reset>".format(info, message)
            status = status.rjust(len(status) + const.OFFSET)
            status = ansi_tran.sub(status)
            print(status)
        else:
            status = "✗ {}: <red>Fail<reset>".format(info)
            status = status.rjust(len(status) + const.OFFSET)
            status = ansi_tran.sub(status)
            print(status)
            err_status = tmp_puller.error_proc.stderr.decode('UTF-8')
            # TODO: duplicate the retrieve_stdout method, merge them
            err_status = err_status.rjust(len(err_status) + const.OFFSET + 2)
            print(err_status)
        del a_spinner
        del tmp_puller
        del tmp_hasher
        # TODO: Add a verbose flag that allow to see the hash range


def remove_cmd(**kwargs):
    """This function is launched when the ``vimpck remove``
    command is invoked.
    """

    vimpckrc = utils.ConfigFile()
    plugls = utils.DiskPlugin(vimpckrc.pack_path)
    ansi_tran = ansi.Parser(const.LHS, const.RHS)

    title = "<bold>:: Removing {} plugin(s)...<reset>".format(len(kwargs['plug']))
    print(ansi_tran.sub(title))

    for plug in kwargs['plug']:
        info = "Removing {}".format(plug)
        a_spinner = spinner.Spinner(info, const.INTERVAL,
                                    const.SEQUENCE, const.OFFSET)
        a_spinner.start()
        if plug in plugls.all_plug.keys():
            try:
                shutil.rmtree(os.path.join(vimpckrc.pack_path, plug))
            except:
                status = "✗ {}: <red>Could not remove !<reset>".format(info)
            else:
                status = "Removed"
                status = "✓ {}: <green>{}<reset>".format(info, status)

            if kwargs['r']:
                vimpckrc.config[const.SECT_2].pop(plugls.all_plug[plug], None)
                vimpckrc.config.write()
        else:
            status = "✗ {}: <red>Not a valid plugin !<reset>".format(info)
        a_spinner.stop()
        status = status.rjust(len(status) + const.OFFSET)
        print(ansi_tran.sub(status))
        del a_spinner
# TODO: spinner class, stop the spinner thread when deleting the object.
# __del__ method


def clean_cmd():
    """This function is launched when the ``vimpck clean``
    command is invoked.
    """
    vimpckrc = utils.ConfigFile()
    plugls = utils.DiskPlugin(vimpckrc.pack_path)

    diff = set(vimpckrc.rem_urls).symmetric_difference(set(plugls.all_plug.values()))

    if not diff:
        sys.exit("no plugins to be removed!")

    ansi_tran = ansi.Parser(const.LHS, const.RHS)
    title = "<bold>:: Removing {} plugin(s)...<reset>".format(len(diff))
    print(ansi_tran.sub(title))
    for rem_url in diff:
        plug = [k for k, v in plugls.all_plug.items() if v == rem_url][0]
        info = "Removing {}".format(plug)
        a_spinner = spinner.Spinner(info, const.INTERVAL,
                                    const.SEQUENCE, const.OFFSET)
        a_spinner.start()
        try:
            shutil.rmtree(os.path.join(vimpckrc.pack_path, plug))
            pass
        except:
            status = "✗ {}: <red>Could not remove!<reset>".format(info)
        else:
            status = "Removed"
            status = "✓ {}: <green>{}<reset>".format(info, status)
        a_spinner.stop()
        status = status.rjust(len(status) + const.OFFSET)
        print(ansi_tran.sub(status))
        del a_spinner
