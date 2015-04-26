from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jsonfield import JSONField
import re

STARTER_CODE = """
/*
on_post is called when a user you are following makes a post.

Pro Tip: You can follow yourself for easier testing
*/
function on_post(input) {
    var post_id = input.post.id;
    var content = input.post.content;
    var poster = input.post.user;
    var date = input.post.date;
    
    /*
    This is your persistent data storage. You can edit it
    directly using the editor next to the code editor.
    To update it here, you must pass it back as output.data
    */
    var data = input.data;

    var output = {};

    /*
    These keys for output are actually optional,
    if you do not want to perform any action
    of matching type.
    */
    output.posts = [];
    output.comments = [];
    output.follow = [];
    output.unfollow = [];
    output.log = [];
    output.data = data


    /*
    // Write a new post like this:

    new_post = {"content": "Hello World! #justprogrammerthings"};
    output.posts.push(new_post);
    

    // Write a comment like this:
    
    response = "Well said, @"+poster;
    new_comment = {"content": response, "post_id": post_id};
    output.comments.push(new_comment);
    
    
    // Follow someone like this:
    
    output.follow.push("my_bff");


    // Unfollow someone like this:

    output.unfollow.push("gary_oak");


    // Log something like this:

    output.log.push("Dear Diary, Today is a good day.");


    // Access and update your data like this:

    var num = data.example_num;
    num += 1;
    data.example_num = num;
    var new_num = 42;
    data.new_num = new_num;
    // save the changes by passing it back as output.data
    output.data = data;

    // Check out some examples by clicking Help or Docs for more info!

    */


    return output;
}

/*
on_comment is called when someone comments on a post you made
*/
function on_comment(input) {
    var content = input.comment.content;
    var commenter = input.comment.user;
    var date = input.comment.date;
    var parent_post = input.comment.parent_post;
    var parent_post_content = parent_post.content;
    var parent_post_poster = parent_post.user;

    var data = input.data;

    var output = {};
    output.posts = [];
    output.comments = [];
    output.follow = [];
    output.unfollow = [];
    output.log = [];
    output.data = data


    /*
    See on_post for the schema for output
    */

    return output;
}

/*
on_mention is called when someone mentions you in their post.

The input for on_mention is exactly the same as the input for on_post.
If an event satisfies the conditions for both on_post and on_mention,
and on_post is active, then only on_post will be called.
*/
function on_mention(input) {
    var post_id = input.post.id;
    var content = input.post.content;
    var poster = input.post.user;
    var date = input.post.date;

    var data = input.data;

    var output = {};
    output.posts = [];
    output.comments = [];
    output.follow = [];
    output.unfollow = [];
    output.log = [];
    output.data = data


    /*
    See on_post for the schema for output
    */

    return output;
}


/*
on_follow is called when someone starts following you
*/
function on_follow(input) {
    var follower_username = input.follower;

    var data = input.data;

    var output = {};
    output.posts = [];
    output.comments = [];
    output.follow = [];
    output.unfollow = [];
    output.log = [];
    output.data = data


    /*
    See on_post for the schema for output
    */

    return output;
}
"""

STARTER_DATA = {"example_num":42, "example_str": "hello", "example_list":[1,2,"three"]}





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

        tag_strings = set(re.findall(r'(?:^|\s)#(\w+)',self.content))
        mention_strings = set(re.findall(r'(?:^|\s)@(\w+)',self.content))

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





class Comment(models.Model):
    content = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)
    mentioned = models.ManyToManyField(User, related_name="mentioning_comments")

    class Meta:
        ordering=['id']

    def save(self, *args, **kwargs):
        super(Comment,self).save(*args,**kwargs)

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

        super(Comment,self).save()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField(Post)
    comments = models.ManyToManyField(Comment)

    
class Script(models.Model):
    userprofile = models.OneToOneField(UserProfile)

    code = models.TextField(default = STARTER_CODE, max_length=5000, blank=True)
    
    data = JSONField(default = STARTER_DATA, blank=True)

    on_post = models.BooleanField(default = False)
    on_comment = models.BooleanField(default = False)
    on_follow = models.BooleanField(default = False)
    on_mention = models.BooleanField(default = False)

    public = models.BooleanField(default= False)



class LogEntry(models.Model):
    content = models.TextField(max_length=1000)
    userprofile = models.ForeignKey(UserProfile)
    date = models.DateTimeField(auto_now_add=True)
    func_input = models.TextField(max_length=1000, blank=True)
    func_output = models.TextField(max_length=1000, blank=True)
    func = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering=['id']

