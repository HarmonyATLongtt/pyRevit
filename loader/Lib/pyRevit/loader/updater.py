# todo: add support for versioning based on git head hash
# todo: test for extensions

import sys
import clr
from collections import namedtuple

from ..logger import get_logger
logger = get_logger(__name__)

from ..config import HOME_DIR
from ..git import git

from System import DateTime, DateTimeOffset


# Generic named tuple for passing repository information to other modules
PyRevitRepoInfo = namedtuple('PyRevitRepoInfo', ['directory', 'head_name', 'last_commit_hash', 'repo'])


def hndlr(url, uname, types):
    up = git.UsernamePasswordCredentials()
    up.Username = 'eirannejad@gmail.com'
    up.Password = 'ehsan2010'
    return up


def _make_pull_options():
    pull_ops = git.PullOptions()
    pull_ops.FetchOptions = git.FetchOptions()
    pull_ops.FetchOptions.CredentialsProvider = git.Handlers.CredentialsHandler(hndlr)
    return pull_ops


def _make_fetch_options():
    fetch_ops = git.FetchOptions()
    fetch_ops.CredentialsProvider = git.Handlers.CredentialsHandler(hndlr)
    return fetch_ops


def _make_pull_signature():
    return git.Signature('eirannejad', 'eirannejad@gmail.com', DateTimeOffset(DateTime.Now))


def find_all_pkg_repos():
    logger.debug('Finding installed repos.')
    repo = git.Repository(HOME_DIR)
    repo_info = PyRevitRepoInfo(repo.Info.WorkingDirectory, repo.Head.Name, repo.Head.Tip.Id.Sha, repo)
    repos = [repo_info]
    logger.debug('Installed repos: {}'.format(repos))
    return repos


def update_pyrevit():
    for repo_info in find_all_pkg_repos():
        repo = repo_info.repo
        logger.debug('Updating repo: {}'.format(repo_info.directory))
        head_msg = str(repo.Head.Tip.Message).replace('\n','')
        logger.debug('Current head is: {} > {}'.format(repo.Head.Tip.Id.Sha, head_msg))
        try:
            repo.Network.Pull(_make_pull_signature(), _make_pull_options())
            logger.debug('Successfully updated repo: {}'.format(repo_info.directory))
            head_msg = str(repo.Head.Tip.Message).replace('\n','')
            logger.debug('New head is: {} > {}'.format(repo.Head.Tip.Id.Sha, head_msg))
            return True
        except Exception as pull_err:
            logger.error('Failed updating: {} | {}'.format(repo_info.directory, pull_err))

    return False

def has_pending_updates(repo_info):
    repo = repo_info.repo
    logger.debug('Fetching updates for: {}'.format(repo_info.directory))
    repo_branches = repo.Branches
    logger.debug('Repo branches: {}'.format([b for b in repo_branches]))

    for remote in repo.Network.Remotes:
        logger.debug('Fetching remote: {} of {}'.format(remote.Name, repo_info.directory))
        try:
            repo.Network.Fetch(remote, _make_fetch_options())
        except Exception as fetch_err:
            logger.error('Failed fetching: {} | {}'.format(repo_info.directory, fetch_err))

    for branch in repo_branches:
        if not branch.IsRemote:
            logger.debug('Comparing heads: {} of {}'.format(branch.CanonicalName, branch.TrackedBranch.CanonicalName))
            hist_div = repo.ObjectDatabase.CalculateHistoryDivergence(branch.Tip, branch.TrackedBranch.Tip)
            if hist_div.BehindBy > 0:
                return True

    return False
