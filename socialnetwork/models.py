from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(null=True, blank=True)
    bio = models.CharField(max_length=430, null=True, blank=True)
    picture_url = models.CharField(blank=True, max_length=256)
    following = models.ManyToManyField(User, related_name="followers")





class Post(models.Model):
    content = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.content, self.user.username, self.date)
    
    class Meta:
        ordering=['id']



class Comment(models.Model):
    content = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)

    class Meta:
        ordering=['id']

