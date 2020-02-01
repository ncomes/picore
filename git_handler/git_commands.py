#import github
import git
import os
# or using an access token
#g = Github("access_token")

# Github Enterprise with custom hostname
#g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

class GitClient:
	def __init__(self):
		pass

	def get_repos(self, username, password):
		g = github.Github(username, password)
		git_info = g.get_users().get_repros()
		repos = [x.name for x in git_info]
		print(repos)
		return repos

	def pull(self, git_dir):
		#g = git.cmd.Git(git_dir)
		#g.pull()

		if os.path.isdir(git_dir):
			repo = git.Repo(git_dir)
			repo.git.pull('origin', 'master')

		return

	def commit(self, git_dir, file_names=[]):
		repo = git.Repo(git_dir)
		repo.config_writer().set_value('user', 'name', 'ncomes').release()
		repo.config_writer().set_value('user', 'email', 'nathancomes@gmail.com').release()
		if not file_names:
			for file in repo.untracked_files:
				file_names.append(file)
				repo.git.add(file)

		repo.git.commit(file_names)
		#repo.git.commit('-m', 'Auto Commit')
		repo.git.push('origin', 'master')
		return




#GIT_DIR = r'/home/pi/picore'
#git_commit(GIT_DIR)

