"""git.py module contains object related to git operation

   Design: A base class named 'Git' with specialized class named after the git
   command 'Clone', 'Pull',... using polymorphism principle of oop paradigm
"""

import subprocess


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
        - local_dir (str): local dir of the copy of the remote repository
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

    Retrieve remote repository
    """

    def __init__(self, remote_url, local_dir):
        super().__init__(local_dir)
        self.remote_url = remote_url

    def git_cmd(self):
        """launch git clone command"""

        cmd = ["git", "-C", self.local_dir, "clone", self.remote_url]
        # TODO: check if .gitmodules is present. If it is launch the command
        # that init all submodules
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class Pull(Git):
    """git pull command"""

    def __init__(self, local_dir):
        super().__init__(local_dir)

    def git_cmd(self):
        """launch git pull command

        Update local repository
        """

        cmd = ["git", "-C", self.local_dir, "pull"]
        # TODO: see if this command also pull the submodule. No it does not.
        # For repo that has submodule, git submodule update --recursive need to
        # be called
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class RevList(Git):
    """git rev-list command

    Retrieve the current hash of the working tree in a local git repository
    """

    def __init__(self, local_dir):
        super().__init__(local_dir)

    def git_cmd(self):
        """launch git rev-list -1 HEAD command"""

        cmd = ["git", "-C", self.local_dir, "rev-list", "-1", "HEAD"]
        out, self.compl_proc, self.error_proc = ex_subprocess(cmd)
        return out


class Log(Git):
    """git log command

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


# Quick testing
if __name__ == "__main__":

    print(":: Test Clone...")
    test = Clone('https://github.com/nicodebo/vim-pck', '/tmp')
    if test.git_cmd() == 1:
        print('not ok')
        print(test.error_proc)
    else:
        print('ok')
        print(test.retrieve_stdout())

    print(":: Test Pull...")
    test2 = Pull('/tmp/vim-pck')
    if test2.git_cmd() == 1:
        print('not ok')
        print(test2.error_proc)
    else:
        print('ok')
        print(test2.retrieve_stdout())

    print(":: Test RevList...")
    test3 = RevList('/tmp/vim-pck')
    if test3.git_cmd() == 1:
        print('not ok')
        print(test3.error_proc)
    else:
        print('ok')
        print(test3.retrieve_stdout())

    print(":: Test Log...")
    test4 = Log('/tmp/vim-pck', '4b6a95fe14a08fd9bae7930e2cea1a1081509ee7',
                'a46335e7982f8ff418c2449df4892e61d024137b')
    if test4.git_cmd() == 1:
        print('not ok')
        print(test4.error_proc)
    else:
        print('ok')
        print(test4.retrieve_stdout())

    print(":: Test IsGitWorkTree, is a git repo: True...")
    test5 = IsGitWorkTree('/tmp/vim-pck')
    if test5.git_cmd() == 1:
        print('not ok')
        print(test4.error_proc)
    else:
        print('ok')
        print(test4.retrieve_stdout())

    print(":: Test IsGitWorkTree, is a git repo: False...")
    test6 = IsGitWorkTree('/tmp')
    if test6.git_cmd() == 1:
        print('not ok')
        print(test4.error_proc)
    else:
        print('ok')
        print(test4.retrieve_stdout())

