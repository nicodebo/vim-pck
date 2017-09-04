import os
import re
import subprocess

from vim_pck import git


def test_humanish():
    """ Test of git.humanish function
    The remote_urls comes from the git manual
    """

    remote_urls = ["ssh://user@host.xz:port/path/to/repo.git/"
                   "git://host.xz:port/path/to/repo.git/",
                   "https://host.xz:port/path/to/repo.git/",
                   "ftps://host.xz:port/path/to/repo.git/",
                   "user@host.xz:path/to/repo.git/",
                   "ssh://user@host.xz:port/~user/path/to/repo.git/",
                   "git://host.xz:port/~user/path/to/repo.git/",
                   "user@host.xz:/~user/path/to/repo.git/",
                   "/path/to/repo.git/",
                   "file:///path/to/repo.git/"]

    for remote_url in remote_urls:
        if git.humanish(remote_url) == "repo":
            assert 1
        else:
            assert 0


class Test_Clone():
    """ Test Clone class """

    def test_valid_address_no_submodule(self, temp_dir):
        """ valid remote url, no submodules """
        bsdir = str(temp_dir.mktemp("test_Clone_class"))
        obj = git.Clone('https://github.com/nicodebo/vim-pck', bsdir)
        out = obj.git_cmd()
        # check that git clone return 0
        assert not out

    def test_valid_address_submodule(self, temp_dir):
        """ valid remote url, no submodules """
        remote_url = 'https://github.com/nicodebo/iron.nvim'
        bsdir = str(temp_dir.mktemp("test_Clone_class"))
        local_dir = os.path.join(bsdir, remote_url.rsplit('/', 1)[-1])
        obj = git.Clone(remote_url, bsdir)
        # check that git clone return 0
        out = obj.git_cmd()
        assert not out
        # check that submodule has been initialized
        cmd = ["git", "-C", local_dir, "submodule", "status"]
        compl_proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
        stdout = compl_proc.stdout.decode('UTF-8').rstrip()
        pattern = r"^\+"
        match = re.search(pattern, stdout)
        if match:
            assert 0
        else:
            assert 1

    def test_non_valid_address(self, temp_dir):
        """ wrong remote url """
        bsdir = str(temp_dir.mktemp("test_Clone_class"))
        obj = git.Clone('https://nonvalidremote/url', bsdir)
        out = obj.git_cmd()
        assert out


class Test_Pull():
    """ Test Pull class """

    def test_valid_address(self, temp_dir):
        """ valid remote url """
        remote_url = 'https://github.com/nicodebo/vim-pck'
        bsdir = str(temp_dir.mktemp("test_Pull_class"))
        local_dir = os.path.join(bsdir, remote_url.rsplit('/', 1)[-1])
        cmd = ["git", "clone", remote_url, local_dir]
        compl_proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
        obj = git.Pull(local_dir)
        out = obj.git_cmd()
        # check that git clone return 0
        assert not out

    def test_non_valid_address(self, temp_dir):
        """ not a git repository """
        remote_url = 'https://nonvalidremote/url'
        bsdir = str(temp_dir.mktemp("test_Pull_class"))
        local_dir = os.path.join(bsdir, remote_url.rsplit('/', 1)[-1])
        os.makedirs(local_dir, exist_ok=True)
        obj = git.Pull(local_dir)
        out = obj.git_cmd()
        # check that git clone return 1
        assert out


class Test_GetRemote():
    """ Test GetRemote class """

    def test_valid_address(self, temp_dir):
        """ valid remote url """
        remote_url = 'https://github.com/nicodebo/vim-pck'
        bsdir = str(temp_dir.mktemp("test_Pull_class"))
        local_dir = os.path.join(bsdir, remote_url.rsplit('/', 1)[-1])
        cmd = ["git", "clone", remote_url, local_dir]
        compl_proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
        obj = git.GetRemote(local_dir)
        out = obj.git_cmd()
        # check that git clone return 0
        assert not out
        assert obj.retrieve_stdout() == remote_url

    def test_non_valid_address(self, temp_dir):
        """ not a git repository """
        remote_url = 'https://nonvalidremote/url'
        bsdir = str(temp_dir.mktemp("test_Pull_class"))
        local_dir = os.path.join(bsdir, remote_url.rsplit('/', 1)[-1])
        os.makedirs(local_dir, exist_ok=True)
        obj = git.GetRemote(local_dir)
        out = obj.git_cmd()
        # check that git clone return 1
        assert out


class Test_Hash():
    """ Test Hash class """

    def test_valid_address(self, temp_dir):
        """ valid remote url """
        remote_url = 'https://github.com/nicodebo/vim-pck'
        bsdir = str(temp_dir.mktemp("test_Hash_class"))
        local_dir = os.path.join(bsdir, remote_url.rsplit('/', 1)[-1])
        ref = "0ab83e7aa0b628d19bb608bdbe6a8bd2c4e78aaa"
        cmd = ["git", "clone", remote_url, local_dir]
        compl_proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
        cmd = ["git", "-C", local_dir, "reset", "--hard", ref]
        compl_proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
        obj = git.Hash(local_dir)
        out = obj.git_cmd()
        # check that git clone return 0
        assert not out
        assert obj.retrieve_stdout() == ref

    def test_non_valid_address(self, temp_dir):
        """ non valid remote url """
        remote_url = 'https://nonvalidremote/url'
        bsdir = str(temp_dir.mktemp("test_Hash_class"))
        local_dir = os.path.join(bsdir, remote_url.rsplit('/', 1)[-1])
        os.makedirs(local_dir, exist_ok=True)
        obj = git.Hash(local_dir)
        out = obj.git_cmd()
        # check that git clone return 1
        assert out
