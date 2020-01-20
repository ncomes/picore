import github

# or using an access token
#g = Github("access_token")

# Github Enterprise with custom hostname
#g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

def get_repos(username, password):
	g = github.Github(username, password)
	git_info = g.get_users().get_repros()
	repos = [x.name for x in git_info]
	return repos

