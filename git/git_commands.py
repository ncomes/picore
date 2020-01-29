#import github
import git
import os
# or using an access token
#g = Github("access_token")

# Github Enterprise with custom hostname
#g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

def get_repos(username, password):
	g = github.Github(username, password)
	git_info = g.get_users().get_repros()
	repos = [x.name for x in git_info]
	return repos

def git_pull(git_dir):
	#g = git.cmd.Git(git_dir)
	#g.pull()

	if os.path.isdir(git_dir):
		repo = git.Repo(git_dir)
		repo.git.pull('origin', 'master')

	return

def git_commit(git_dir):
	repo = git.Repo(git_dir)
	repo.config_writer().set_value('user', 'name', 'ncomes').release()
	repo.config_writer().set_value('user', 'email', 'nathancomes@gmail.com').release()
	#repo.config_writer().set_value('user', 'password', 'nate3022').release()

	for file in repo.untracked_files:
		repo.git.add(file)

	repo.git.commit('-m', 'Auto Commit')
	repo.git.push('origin', 'master')
	return

GIT_DIR = r'/home/pi/picore'
git_commit(GIT_DIR)

