import os
import io
import subprocess


from loguru import logger


from threatingestor.sources import Source
from threatingestor.exceptions import DependencyError


try:
    subprocess.check_output('git')
except FileNotFoundError:
    raise DependencyError("System dependency Git required for Git source is not installed")
except subprocess.CalledProcessError:
    # Non-zero exit codes are fine.
    pass


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
        # Initialize.
        new_hash = saved_state
        all_filenames = []

        if saved_state:
            # Pull and diff to get filenames.
            try:
                _git_pull(self.local_path)
                new_hash = _git_latest_hash(self.local_path)
                all_filenames = _git_diff_names(self.local_path, saved_state).splitlines()
            except (OSError, subprocess.CalledProcessError):
                logger.exception(f"Error with git pull from '{self.local_path}'")

        else:
            # First run, we try cloning the repo and look at all files.
            try:
                _git_clone(self.url, self.local_path)
                new_hash = _git_latest_hash(self.local_path)
                all_filenames = _git_ls_files(self.local_path).splitlines()

            except subprocess.CalledProcessError:
                # Clone failed, maybe the repo already exists?
                # If so, update the saved state so we can pull on the next run.
                try:
                    new_hash = _git_latest_hash(self.local_path)

                except (OSError, subprocess.CalledProcessError):
                    # That also failed, so this is just a generic error.
                    logger.exception(f"Error with git clone of '{self.url}' to '{self.local_path}'")

            except OSError:
                logger.exception(f"Error with git clone of '{self.url}' to '{self.local_path}'")

        # If not modified or any errors, return immediately.
        if saved_state == new_hash:
            return saved_state, []

        # Otherwise, process YARA files.
        artifact_list = []
        for filename in all_filenames:
            if any([filename.endswith(x) for x in YARA_FILE_EXTS]):
                try:
                    with io.open(os.path.join(self.local_path, filename), 'r', encoding='utf-8', errors='ignore') as f:
                        artifact_list += self.process_element(f.read(), self.url, include_nonobfuscated=True)
                except OSError:
                    # The file was most likely deleted.
                    pass

        return new_hash, artifact_list


def _git_cmd(args):
    """Call a git command.

    :raises: subprocess.CalledProcessError
    """
    git_cmdline = ['git'] + args
    return subprocess.check_output(git_cmdline).decode('utf-8')


def _git_cmd_chdir(path, args):
    cwd = os.getcwd()
    os.chdir(path)
    output = _git_cmd(args)
    os.chdir(cwd)
    return output


def _git_clone(remote, local_path):
    return _git_cmd(['clone', '--', remote, local_path])


def _git_latest_hash(local_path):
    return _git_cmd_chdir(local_path, ['rev-parse', 'HEAD']).strip()


def _git_pull(local_path):
    return _git_cmd_chdir(local_path, ['pull'])


def _git_diff_names(local_path, prev_hash):
    return _git_cmd_chdir(local_path, ['diff', '--name-only', prev_hash])


def _git_ls_files(local_path):
    return _git_cmd_chdir(local_path, ['ls-files'])
