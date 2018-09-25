import requests,json

def count_user_commits(user):
	r = requests.get('https://github.univar.com/api/v3/repos'% user)
	repos = json.loads(r.content)

	for repo in repos:
		n = count_repo_commits(repo['url'] + '/commits')
		repo['num_commits'] = n
		yield repo

def count_repo_commits(commit_url,_acc=0):
	r = requests.get(commits_url)
	commits = json.loads(r.content)
	n = len(commits)
	if n == 0:
		return _acc
	next_url = find_next(r.headers['link'])
	if next_url is None:
		return _acc + n
	return count_repo_commits(next_url, _acc + n)

def find_next(link):
    for l in link.split(','):
        a, b = l.split(';')
        if b.strip() == 'rel="next"':
            return a.strip()[1:-1]

if __name__ == '__main__':
	total = 0
	for repo in count_user_commits(user):
		print "Repo`%(name)s` has %(num_commits)d commits" % repo
		total += repo['num_commits']
	print "Total commits: %d" %total
