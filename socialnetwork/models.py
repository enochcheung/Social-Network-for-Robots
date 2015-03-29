from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jsonfield import JSONField
import re

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(null=True, blank=True)
    bio = models.CharField(max_length=430, null=True, blank=True)
    picture_url = models.CharField(blank=True, max_length=256)
    following = models.ManyToManyField(User, related_name="followers")

    def natural_key(self):
        return self.user.natural_key()



class Post(models.Model):
    content = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    mentioned = models.ManyToManyField(User, related_name="mentioning_posts")

    def __unicode__(self):
        return "%s - %s (%s)" % (self.content, self.user.username, self.date)
    
    def save(self, *args, **kwargs):
        super(Post,self).save(*args,**kwargs)

        tag_strings = set(re.findall(r'#(\w+)',self.content))
        mention_strings = set(re.findall(r'@(\w+)',self.content))

        for tag_string in tag_strings:
            try:
                tag = Tag.objects.get(name=tag_string)
            except Tag.DoesNotExist:
                tag = Tag(name=tag_string)
                tag.save()

            self.tag_set.add(tag)

        for username in mention_strings:
            try:
                user = User.objects.get(username=username)
                self.mentioned.add(user)
            except User.DoesNotExist:
                pass

        super(Post,self).save()


    class Meta:
        ordering=['id']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField(Post)



class Comment(models.Model):
    content = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)

    class Meta:
        ordering=['id']


class Script(models.Model):
    userprofile = models.OneToOneField(UserProfile)

    code = models.TextField(max_length=5000, blank=True)
    
    data = JSONField(default={}, blank=True)

    on_post = models.BooleanField(default = False)
    on_comment = models.BooleanField(default = False)
    on_follow = models.BooleanField(default = False)
    on_mention = models.BooleanField(default = False)



class LogEntry(models.Model):
    content = models.TextField(max_length=1000)
    userprofile = models.ForeignKey(UserProfile)
    date = models.DateTimeField(auto_now_add=True)
    func_input = models.TextField(max_length=1000, blank=True)
    func_output = models.TextField(max_length=1000, blank=True)
    func = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering=['id']
