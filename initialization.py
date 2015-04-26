from socialnetwork.models import *
usernames = ['Jules','todo']
for username in usernames:
	user = UserProfile.objects.get(user__username = username)
	user.script.public = True
	user.script.save()

