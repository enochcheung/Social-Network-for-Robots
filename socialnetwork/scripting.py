from django.db import transaction

from socialnetwork.models import UserProfile, Post, Comment, Script, LogEntry, Tag
from socialnetwork.forms import PostForm, CommentForm

import execjs
import traceback
import json
from threading import Thread

MULTITHREAD = True

def on_post(post):
	if MULTITHREAD:
		t = Thread(target=on_post_thread, args=[post])
		t.daemon = False
		t.start()

	else:
		on_post_thread(post)

def on_comment(comment):
	if MULTITHREAD:
		t = Thread(target=on_comment_thread, args=[comment])
		t.daemon = False
		t.start()

	else:
		on_comment_thread(post)

def on_follow(follower,followee):
	if MULTITHREAD:
		t = Thread(target=on_follow_thread, args=[follower,followee])
		t.daemon = False
		t.start()

	else:
		on_thread_thread(follower,followee)



def on_post_thread(post):
	poster = post.user
	followersprofiles = poster.followers.all()
	mentioned = post.mentioned.all()
	served = set()

	for followerprofile in followersprofiles:
		follower = followerprofile.user

		if follower not in served:
			served.add(follower)
			script = followerprofile.script

			if script.on_post:
				run_script_post(post,follower)

	for user in mentioned:
		if user not in served:
			served.add(user)
			script = user.userprofile.script

			if script.on_post:
				run_script_mention(post,user)




def on_comment_thread(comment):
	parent_post_poster = comment.post.user

	script = comment.post.user.userprofile.script

	if script.on_comment:
		run_script_comment(comment,parent_post_poster)


def on_follow_thread(follower,followee):

	script = followee.userprofile.script
	if script.on_follow:
		run_script_follow(follower,followee)


@transaction.atomic
def run_script_post(post, user):
	script = user.userprofile.script

	func_input = {}
	

	func_input['post'] = serialize_post(post)
	func_input['data'] = script.data		# TODO: should select_for_update lock

	code = script.code

	errorlogger = ErrorLogger('on_post',user)
	errorlogger.func_input = json.dumps(func_input)

	try:

		response = run_script(code,'on_post',func_input, errorlogger)

		errorlogger.func_output= json.dumps(response)
	

		handle_response(response,user,errorlogger)
	except:
		errorlogger.log_error("Error: Unknown Error")
		print traceback.format_exc()


@transaction.atomic
def run_script_mention(post,user):
	script = user.userprofile.script

	func_input = {}
	

	func_input['post'] = serialize_post(post)
	func_input['data'] = script.data		# TODO: should select_for_update lock

	code = script.code

	errorlogger = ErrorLogger('on_mention',user)
	errorlogger.func_input = json.dumps(func_input)

	try:

		response = run_script(code,'on_mention',func_input, errorlogger)

		errorlogger.func_output= json.dumps(response)
	

		handle_response(response,user,errorlogger)
	except:
		errorlogger.log_error("Error: Unknown Error")
		print traceback.format_exc()


@transaction.atomic
def run_script_comment(comment,user):
	script = user.userprofile.script
	func_input={}
	func_input['comment']=serialize_comment(comment)
	func_input['data']=script.data
	code = script.code

	errorlogger = ErrorLogger('on_comment',user)
	errorlogger.func_input = json.dumps(func_input)

	response = run_script(code,'on_comment',func_input,errorlogger)

	try:
		errorlogger.func_output= json.dumps(response)
	except:
		print "error logging func_output"

	handle_response(response,user,errorlogger)


@transaction.atomic
def run_script_follow(follower,user):
	script = user.userprofile.script
	func_input={}
	func_input['follower']=follower.username
	func_input['data']=script.data
	code = script.code

	errorlogger = ErrorLogger('on_follow',user)
	errorlogger.func_input = json.dumps(func_input)

	response = run_script(code,'on_follow',func_input,errorlogger)

	try:
		errorlogger.func_output= json.dumps(response)
	except:
		print "error logging func_output"

	handle_response(response,user,errorlogger)



def serialize_post(post):
	post_info = {}
	post_info['content'] = post.content
	post_info['user'] = post.user.username
	post_info['date'] = str(post.date)
	post_info['id'] = post.id
	post_info['mentioned'] = map(lambda user: {'username':user.username},
								post.mentioned.all())
	post_info['tags'] = map(lambda tag: {'name':tag.name},
							post.tag_set.all())

	return post_info

def serialize_comment(comment):
	comment_info = {}
	comment_info['content'] = comment.content
	comment_info['user'] = comment.user.username
	comment_info['date'] = str(comment.date)
	comment_info['id'] = comment.id
	comment_info['parent_post'] = serialize_post(comment.post)

	return comment_info



def run_script(code, func_name, func_input, errorlogger) :
	sandboxcode = """
	"use strict";
	var vm = require('vm');

	function safe_run(code, func_name, input) {
		var vm_output = [];
		var sandbox = {	vm_input : input,
						vm_output: vm_output,
						require : function() {throw Error('require not allowed');}}
		vm.createContext(sandbox);
		vm.runInContext('"use strict";\\n'+code,sandbox,{'timeout':200});
		vm.runInContext('vm_output.push('+func_name+'(vm_input))',sandbox,{'timeout':200});


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
		errorlogger.log_error(str(e))
		return {}
	except:
		print traceback.format_exc()
		errorlogger.log_error('Error: Unknown Error')
		return {}

	return response


class ErrorLogger():
	def __init__(self, func, user, func_input=None, func_output=None):
		self.func = func
		self.user = user
		self.func_input = func_input
		self.func_output = func_output


	@transaction.atomic
	def log_error(self,message):
		log_entry = LogEntry(content = message, userprofile = self.user.userprofile, func=self.func)
		if self.func_input:
			log_entry.func_input = self.func_input
		if self.func_output:
			log_entry.func_output = self.func_output

		log_entry.save()

@transaction.atomic
def handle_response(response, user, errorlogger):
	# TODO: validate format of response

	if 'data' in response:

		## validate response

		new_data = response['data']
		script = user.userprofile.script
		script.data = new_data
		script.save()


	if 'posts' in response:
		for post_info in response['posts']:
			if 'content' not in post_info:
				errorlogger.log_error("Error: Invalid post: "+json.dumps(post_info))
				break

			content = post_info['content']

			post_form = PostForm({'content':content})
			if not post_form.is_valid():
				errorlogger.log_error("Error: Invalid post: "+json.dumps(post_info))
				break

			new_post = Post(content=post_form.cleaned_data['content'], user=user)
			new_post.save()
	
	if 'comments' in response:
		for comment_info in response['comments']:
			if ('content' not in comment_info) or ('post_id' not in comment_info):
				errorlogger.log_error("Error: Invalid comment: "+json.dumps(comment_info))
				break

			post_id = comment_info['post_id']
			content = comment_info['content']
			comment_form = CommentForm({'post':post_id,'content':content})
			if not comment_form.is_valid():
				errorlogger.log_error("Error: Invalid comment: "+json.dumps(comment_info))
				break

			new_comment = Comment(content=comment_form.cleaned_data['content'],
									post=comment_form.cleaned_data['post'],
									user=user)
			new_comment.save()



