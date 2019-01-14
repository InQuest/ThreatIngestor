import os
import io
import sys
import subprocess

from threatingestor.sources import Source

YARA_FILE_EXTS = [
    '.rule',
    '.yar',
    '.yara',
    '.rules',
]

class Plugin(Source):

    def __init__(self, name, url, local_path):
        self.name = name
        self.url = url
        self.local_path = local_path

    def run(self, saved_state):
        # initialize
        new_hash = saved_state
        all_filenames = []

        if saved_state:
            # pull and diff to get filenames
            try:
                git_pull(self.local_path)
                new_hash = git_latest_hash(self.local_path)
                all_filenames = git_diff_names(self.local_path, saved_state).splitlines()
            except (subprocess.CalledProcessError, OSError) as e:
                sys.stderr.write("error with git pull from {path}: {e}".format(path=self.local_path, e=e))

        else:
            # first time, we try cloning the repo and look at all files
            try:
                git_clone(self.url, self.local_path)
                new_hash = git_latest_hash(self.local_path)
                all_filenames = git_ls_files(self.local_path).splitlines()
            except (subprocess.CalledProcessError, OSError) as e:
                sys.stderr.write("error with git clone of {url} to {path}: {e}".format(url=self.url,
                                                                                       path=self.local_path,
                                                                                       e=e))

        # if not modified or any errors, return immediately
        if saved_state == new_hash:
            return saved_state, []

        # otherwise, process yara files
        artifact_list = []
        for filename in all_filenames:
            if any([filename.endswith(x) for x in YARA_FILE_EXTS]):
                with io.open(os.path.join(self.local_path, filename), 'r', encoding='utf-8', errors='ignore') as f:
                    artifact_list += self.process_element(f.read(), self.url, include_nonobfuscated=True)

        return new_hash, artifact_list


def _git_cmd(args):
    # may raise subprocess.CalledProcessError
    git_cmdline = ['git'] + args
    return subprocess.check_output(git_cmdline).decode('utf-8')

def _git_cmd_chdir(path, args):
    cwd = os.getcwd()
    os.chdir(path)
    output = _git_cmd(args)
    os.chdir(cwd)
    return output

def git_clone(remote, local_path):
    return _git_cmd(['clone', '--', remote, local_path])

def git_latest_hash(local_path):
    return _git_cmd_chdir(local_path, ['rev-parse', 'HEAD']).strip()

def git_pull(local_path):
    return _git_cmd_chdir(local_path, ['pull'])

def git_diff_names(local_path, prev_hash):
    return _git_cmd_chdir(local_path, ['diff', '--name-only', '--', prev_hash])

def git_ls_files(local_path):
    return _git_cmd_chdir(local_path, ['ls-files'])
