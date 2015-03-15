from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.core import serializers

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail


from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from socialnetwork.models import Post, UserProfile, Comment, Script
from socialnetwork.forms import RegistrationForm, PostForm, EditProfileForm, CommentForm, ScriptForm
from socialnetwork.s3 import s3_upload, s3_delete
from socialnetwork.scripting import on_post


@login_required
def stream(request):
    context = {}
    context['posts'] = Post.objects.all()[::-1]
    context['post_form'] = PostForm()
    return render(request, 'socialnetwork/stream.html',context)

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form']= RegistrationForm()
        return render(request, 'socialnetwork/register.html',context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    new_user.is_active = False
    new_user.save()


    new_user_profile = UserProfile(user=new_user)
    new_user_profile.save()

    new_script = Script(userprofile=new_user_profile)
    new_script.save()

     # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
    Welcome to the Social Network.  Please click the link below to
    verify your email address and complete the registration of your account:
    http://%s%s
    """ % (request.get_host(), 
       reverse('confirm_registration', args=[new_user.username, token]))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="enochc.socialnetwork@gmail.com",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']


    # Logs in the new user and redirects to global stream
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    # login(request, new_user)

    context={}
    context['email'] = form.cleaned_data['email']
    return render(request, 'socialnetwork/needs-confirmation.html',context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    return render(request, 'socialnetwork/confirmed.html', {})


@login_required
@transaction.atomic
def post(request):
    context={}
    if request.method == 'GET':
        context['posts'] = Post.objects.all()[::-1]
        context['post_form'] = PostForm()
        return render(request, 'socialnetwork/stream.html',context)

    form = PostForm(request.POST)
    context['form']=form

    if not form.is_valid():
        context['posts'] = Post.objects.all()[::-1]
        return render(request, 'socialnetwork/stream.html',context) 

    new_post = Post(content=form.cleaned_data['content'], user=request.user)
    new_post.save()

    on_post(new_post)

    context['post_form'] = PostForm()
    context['posts'] = Post.objects.all()[::-1]
    return render(request, 'socialnetwork/stream.html', context)
    
@login_required
@transaction.atomic
def comment(request):
    context={}
    if request.method == 'GET':
        return redirect(reverse('stream'))

    form = CommentForm(request.POST)

    if not form.is_valid():
        return redirect(reverse('stream')) 

    new_comment = Comment(content=form.cleaned_data['content'], user=request.user, post=form.cleaned_data['post'])
    new_comment.save()

    return redirect(reverse('stream'))


@login_required
def get_posts(request,start_id=0):
    posts = Post.objects.filter(id__gte=start_id)

    response_text = serializers.serialize('json', posts, use_natural_foreign_keys=True)
    return HttpResponse(response_text,content_type="application/json")

@login_required
def get_comments(request,post_id,start_id=0):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.filter(id__gte=start_id)

    response_text = serializers.serialize('json', comments, use_natural_foreign_keys=True)
    return HttpResponse(response_text,content_type="application/json")


@login_required
def profile(request, username):
    errors=[]
    context = {}
    
    try:
        user = User.objects.get(username=username)
        context['profile_user']=user
        posts = Post.objects.filter(user=user)[::-1]
        context['posts']=posts

        if request.user.userprofile.following.filter(username=user.username):
            context['already_following']=1
    except (User.DoesNotExist):
        errors.append('User '+username+' not found.')





    context['errors']=errors

    return render(request, 'socialnetwork/profile.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    context={}
    if request.method == 'GET':
        
        user = request.user

        initial = {}
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        if user.userprofile.age:
            initial['age'] = user.userprofile.age
        if user.userprofile.bio:
            initial['bio'] = user.userprofile.bio

        form = EditProfileForm(initial=initial)

        context['form'] = form
        return render(request, 'socialnetwork/edit_profile.html',context)

    form = EditProfileForm(request.POST,request.FILES)
    context['form']=form

    if not form.is_valid():
        return render(request, 'socialnetwork/edit_profile.html',context) 

    user = request.user
    if ('first_name' in form.cleaned_data) and form.cleaned_data['first_name']:
        user.first_name = form.cleaned_data['first_name']
    if ('last_name' in form.cleaned_data) and form.cleaned_data['last_name']:
        user.last_name = form.cleaned_data['last_name']
    
    if ('age' in form.cleaned_data) and form.cleaned_data['age']:
        user.userprofile.age = form.cleaned_data['age']
    if ('bio' in form.cleaned_data) and form.cleaned_data['bio']:
        user.userprofile.bio = form.cleaned_data['bio']

    if ('picture' in form.cleaned_data) and form.cleaned_data['picture']:
        if form.cleaned_data['picture']:
            url = s3_upload(form.cleaned_data['picture'], user.id)
            user.userprofile.picture_url = url

    if ('password1' in form.cleaned_data) and form.cleaned_data['password1']:
        user.set_password(form.cleaned_data['password1'])


    user.userprofile.save()
    user.save()

    if ('password1' in form.cleaned_data) and form.cleaned_data['password1']:
        new_user = authenticate(username=user.username,
                            password=form.cleaned_data['password1'])
        login(request, new_user)

    return redirect(reverse('profile', args=[request.user.username]))
    
@login_required
def profile_pic_url(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user':user}
    return render(request, 'socialnetwork/profile_pic_url.txt',context)

@login_required
def scripts(request):
    context={}
    script = request.user.userprofile.script
    form = ScriptForm(request.POST or None, instance = script)
    context['form']=form

    if request.method == 'GET':
        return render(request, 'socialnetwork/scripts.html',context)
    if not form.is_valid():
        print "invalid form"
        return render(request, 'socialnetwork/scripts.html',context)

    form.save()
    return render(request, 'socialnetwork/scripts.html',context)

@login_required
def logs(request):
    context={}
    return render(request, 'socialnetwork/logs.html',context)


@login_required
def follower_stream(request):
    context = {}
    following = request.user.userprofile.following.all()
    context['following'] = following
    context['posts'] = Post.objects.filter(user__in=following)[::-1]
    return render(request, 'socialnetwork/follower_stream.html',context)

@login_required
@transaction.atomic
def follow(request, username):
    self_user = request.user
    user = get_object_or_404(User, username=username)
    self_user.userprofile.following.add(user)

    self_user.userprofile.save()

    return redirect(reverse('follower_stream'))

@login_required
@transaction.atomic
def unfollow(request, username):
    self_user = request.user
    user = get_object_or_404(User, username=username)
    self_user.userprofile.following.remove(user)

    self_user.userprofile.save()

    return redirect(reverse('follower_stream'))




