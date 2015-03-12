from django.db import transaction

from models import UserProfile, Post, Comment, Script
from forms import PostForm, CommentForm

import execjs



def on_post(post):
	poster = post.user
	followers = poster.userprofile.followers

	for follower in followers:
		script = follower.userprofile.script
		if script.on_post_active:
			run_script_poster(post,script)

@transaction.atomic
def run_script_post(post, script):
	context = {}
	post_info = {}
	post_info['content'] = post.content
	post_info['user'] = post.user.username
	post_info['date'] = post.date
	post_info['id'] = post.id

	context['post'] = post_info
	context['database'] = script.database		# TODO: should read/write lock

	js = script.on_post

	try:
		# TODO: timeout

		js_ctx = execjs.get('Node').compile(js);
		response = js_ctx.call('on_post', context)
	except ProgramError as e:
		print str(e)
		return
	except:
		print traceback.format_exc()
		return

	run_response(response,script)
	

def run_response(response,script):
	# TODO: validate format of response


	if 'database' in response:
		new_database = response['database']
		script.database = new_database
		script.save()

	if 'posts' in response:
		for post_info in response['posts']
			# TODO: check formatting

			content = post_info['content']

			post_form = PostForm(content=content)
			if not post_form.is_valid():
				print "invalid response "+ str(response)
				return

			new_post = Post(content=post_form.cleaned_data['content'], user=script.user.user)
    		new_post.save()




