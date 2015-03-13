from django.db import transaction

from models import UserProfile, Post, Comment, Script
from forms import PostForm, CommentForm

import execjs
import traceback



def on_post(post):
	poster = post.user
	followersprofiles = poster.followers.all()

	for followerprofile in followersprofiles:

		script = followerprofile.script
		follower = followerprofile.user

		if script.on_post_active:
			run_script_post(post,follower)

@transaction.atomic
def run_script_post(post, user):
	script = user.userprofile.script

	context = {}
	post_info = {}
	post_info['content'] = post.content
	post_info['user'] = post.user.username
	post_info['date'] = str(post.date)
	post_info['id'] = post.id

	context['post'] = post_info
	context['database'] = script.database		# TODO: should read/write lock

	code = script.code


	response = run_script(code,'on_post',context)

	run_response(response,user)
	


def run_script(code, func_name, func_input) :
	#sandboxcode = open('sandbox.js','r').read()
	sandboxcode = """
	'use strict';
	var vm = require('vm');

	function safe_run(code, func_name, input) {
		var vm_output = [];
		var sandbox = {	vm_input : input,
						vm_output: vm_output,
						require : function() {throw Error('require not allowed');}}
		vm.createContext(sandbox);
		vm.runInContext(code,sandbox);
		vm.runInContext('vm_output.push('+func_name+'(vm_input))',sandbox);


		return vm_output[0];
	}
	"""


	js_ctx = execjs.get('Node').compile(sandboxcode)

	try:
		response = js_ctx.call('safe_run',code,func_name,func_input)
	# except execjs.ProgramError as e:
	# 	print str(e)
	# 	return {'error':str(e)}
	# except execjs.RuntimeError as e:
	# 	print str(e)
	# 	return {'error':str(e)}
	except execjs.Error as e:
		print str(e)
		return {'error':str(e)}
	except:
		print traceback.format_exc()
		return {'error': 'Unknown error'}

	return response


def run_response(response,user):
	# TODO: validate format of response

	if 'error' in response:
		print response

	if 'database' in response:
		new_database = response['database']
		script.database = new_database
		script.save()

	if 'posts' in response:
		for post_info in response['posts']:
			# TODO: check formatting

			content = post_info['content']

			post_form = PostForm({'content':content})
			if not post_form.is_valid():
				print "invalid response "+ str(response)
				return

			new_post = Post(content=post_form.cleaned_data['content'], user=user)

    		new_post.save()




