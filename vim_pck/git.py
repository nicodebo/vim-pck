"""git.py module contains object related to git operation

   Design: A base class named 'Git' with specialized class named after the git
   command 'Clone', 'Pull',... using polymorphism principle of oop paradigm
"""

import subprocess
import re
import os


def humanish(remote_url):
    """Get the humanish part of a remote git url

    equivalent of the following multiexpression sed search and replace:
        sed -e 's|/$||' -e 's|:*/*\.git$||' -e 's|.*[/:]||g'

    https://stackoverflow.com/questions/13839879/how-to-determine-the-humanish-part-of-a-git-repository#13840631
    see man git-clone
    """

    result = remote_url
    regexes = [r"/$", r":*/*\.git$", r".*[/:]"]
    for regex in regexes:
        result = re.sub(regex, "", result)
    return result


def ex_subprocess(cmd):
    """subprocess wrapper function

    Arguments:
            - cmd (list(str)): the command to feed the subprocess

    Return:
        (out, compl_proc, error_proc) (3-uple):
            - out (int) : 1 suprocess fail, 0 subprocess succeed
            - compl_proc (subprocess.CompletedProcess instance): return value
              of the subprocess when it has succeeded
            - error_proc (subprocess.CalledProcessError instance): value of the
              subprocess when an Exception has occured
    """

    out = 1
    compl_proc = None
    error_proc = None

    try:
        compl_proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as error:
        error_proc = error
    else:
        out = 0
    finally:
        return out, compl_proc, error_proc


class Git:
    """The base Git class

    Attributs:
        - remote_url (str):  ex, https://github.com/nicodebo/vimpck
        - local_dir (str): local root directory of the copy of the remote
            repository
        - compl_proc (subprocess.CompletedProcess instance): return value
          of the subprocess when it has succeeded
        - error_proc (subprocess.CalledProcessError instance): value of the
          subprocess when an Exception has occured
    """

    def __init__(self, local_dir):
        self.local_dir = local_dir
        self.error_proc = None
        self.compl_proc = None

    def git_cmd(self):
        """Polymorph method that implement different git command"""
        raise NotImplementedError("Git command method not defined")

    def retrieve_stdout(self):
        """Get the stdout from a completed process instance

        Arguments:
                - comp_proc (subprocess.CompletedProcess instance) : instance
                  that is returned when subprocess.run() function is completed
        """

        return self.compl_proc.stdout.decode('UTF-8').rstrip()


class Clone(Git):
    """git clone command

    Download remote repository

    Attributs:
            - root_dir (str): directory to clone into
    """

    def __init__(self, remote_url, root_dir):
        tmp_path = os.path.join(root_dir, humanish(remote_url))
        super().__init__(tmp_path)
        self.remote_url = remote_url
        self.cmd_sub = [InitSubmodule(tmp_path)]  # object container
        self.root_dir = root_dir

    def git_cmd(self):
        """launch git clone command"""

        cmd = ["git", "clone", self.remote_url, self.local_dir]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)

        git_mod_path = os.path.join(self.local_dir, ".gitmodules")

        if os.path.isfile(git_mod_path) & (out == 0):
            out = self.cmd_sub[0].git_cmd()
            self.compl_proc = self.cmd_sub[0].compl_proc
            self.error_proc = self.cmd_sub[0].error_proc
        return out


class Pull(Git):
    """git pull"""

    def __init__(self, local_dir):
        super().__init__(local_dir)
        self.cmd_sub = [UpdateSubmodule(local_dir)]  # object container

    def git_cmd(self):
        """launch git pull command

        Update local repository
        """

        cmd = ["git", "-C", self.local_dir, "pull"]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)

        git_mod_path = os.path.join(self.local_dir, ".gitmodules")
        if os.path.isfile(git_mod_path) & (out == 0):
            out = self.cmd_sub[0].git_cmd()
            self.compl_proc = self.cmd_sub[0].compl_proc
            self.error_proc = self.cmd_sub[0].error_proc
        return out


class Hash(Git):
    """git rev-list -1 HEAD

    Retrieve the current hash of the working tree in a local git repository
    """

    def __init__(self, local_dir):
        super().__init__(local_dir)

    def git_cmd(self):
        """launch git rev-list -1 HEAD command"""

        cmd = ["git", "-C", self.local_dir, "rev-list", "-1", "HEAD"]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class HistRange(Git):
    """git log <sha(i)>..<sha2(i+n)>

    Return the commit history between 2 hashes
    """

    def __init__(self, local_dir, early_sha, later_sha):
        super().__init__(local_dir)
        self.early_sha = early_sha
        self.later_sha = later_sha

    def git_cmd(self):
        """launch git log --graph --online --decorate sha(n-x)..sha(n+y)
        command
        """

        cmd = ["git", "--no-pager", "-C",
               self.local_dir, "log", "--color",
               "--graph", "--oneline", "--decorate",
               "{0}..{1}".format(self.early_sha, self.later_sha)]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class IsGitWorkTree(Git):
    """git rev-parse --is-inside-work-tree command

    Check if a directory is git repository
    """

    def __init__(self, local_dir):
        super().__init__(local_dir)

    def git_cmd(self):
        """launch command"""
        cmd = ["git", "-C", self.local_dir,
               "rev-parse", "--is-inside-work-tree"]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class GetRemote(Git):
    """git config --get remote.origin.url

    Check if a directory is git repository
    """

    def __init__(self, local_dir):
        super().__init__(local_dir)

    def git_cmd(self):
        """launch command"""
        cmd = ["git", "-C", self.local_dir,
               "config", "--get", "remote.origin.url"]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class InitSubmodule(Git):
    """git submodule update --init --recursive

    install submodule in a already cloned repository
    """

    def __init__(self, local_dir):
        super().__init__(local_dir)

    def git_cmd(self):
        """launch command
        """

        cmd = ["git", "-C", self.local_dir, "submodule", "update", "--init",
               "--recursive"]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class UpdateSubmodule(Git):
    """git submodule update --recursive

    update submodule in a already cloned repository
    """

    def __init__(self, local_dir):
        super().__init__(local_dir)

    def git_cmd(self):
        """launch command
        """

        cmd = ["git", "-C", self.local_dir, "submodule", "update",
               "--recursive"]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


# Quick testing
if __name__ == "__main__":

    def git_test(test_desc, git_inst):
        print(test_desc)
        out = git_inst.git_cmd()
        if out == 1:
            print('not ok')
            print(git_inst.error_proc)
        else:
            print('ok')
            print(git_inst.retrieve_stdout())
        print('\n')
        return out

    clone_obj = Clone('https://github.com/nicodebo/vim-pck', '/tmp')
    git_test(":: Test Clone...", clone_obj)

    clone_obj2 = Clone('https://github.com/hkupty/iron.nvim', '/tmp')
    git_test(":: Test Clone with submodules...", clone_obj2)

    pull_obj = Pull('/tmp/vim-pck')
    git_test(":: Test Pull without submodules...", pull_obj)

    pull_obj2 = Pull('/tmp/iron.nvim')
    git_test(":: Test Pull with submodule...", pull_obj2)

    revlist_obj = Hash('/tmp/vim-pck')
    git_test(":: Test Hash...", revlist_obj)

    log_obj = HistRange('/tmp/vim-pck',
                        '4b6a95fe14a08fd9bae7930e2cea1a1081509ee7',
                        'a46335e7982f8ff418c2449df4892e61d024137b')
    git_test(":: Test HistRange...", log_obj)

    git_wt_obj = IsGitWorkTree('/tmp/vim-pck')
    git_test(":: Test IsGitWorkTree, is a git repo: True...", git_wt_obj)

    git_wt_obj2 = IsGitWorkTree('/tmp')
    git_test(":: Test IsGitWorkTree, is a git repo: False...", git_wt_obj2)

    git_rem_obj = GetRemote('/tmp')
    git_test(":: Test GetRemote, inside a git repo...", git_rem_obj)

    git_rem_obj2 = GetRemote('/tmp/vim-pck')
    git_test(":: Test GetRemote, outside a git repo: True...", git_rem_obj2)

    # test humanish

    remote_url = ["ssh://user@host.xz:port/path/to/repo.git/"
                  "git://host.xz:port/path/to/repo.git/",
                  "https://host.xz:port/path/to/repo.git/",
                  "ftps://host.xz:port/path/to/repo.git/",
                  "user@host.xz:path/to/repo.git/",
                  "ssh://user@host.xz:port/~user/path/to/repo.git/",
                  "git://host.xz:port/~user/path/to/repo.git/",
                  "user@host.xz:/~user/path/to/repo.git/",
                  "/path/to/repo.git/",
                  "file:///path/to/repo.git/"]

    for elem in remote_url:
        if humanish(elem) == "repo":
            print("ok")
            assert 1
        else:
            print("not ok")
            assert 0

# TODO: put all these hereabove tests under pytest

