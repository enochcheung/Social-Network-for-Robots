from django.conf.urls import patterns, include, url
from socialnetwork import views

urlpatterns = patterns('',

    url(r'^$', views.stream, name="home"),
    url(r'^stream/$', views.stream, name="stream"),

    url(r'^login/$', 'django.contrib.auth.views.login', \
    	{'template_name': 'socialnetwork/login.html'}, name="login"),

    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

    url(r'^register/$', views.register, name="register"),
    url(r'^confirm-registration/(?P<username>[^/]+)/(?P<token>[a-z0-9\-]+)$', views.confirm_registration, name="confirm_registration"),


    url(r'^post/$', views.post, name="post"),
    url(r'^comment/$', views.comment, name="comment"),

    url(r'^get_posts/(?P<start_id>\d+)/$', views.get_posts, name="get_posts"),

    url(r'^get_comments/(?P<post_id>\d+)/(?P<start_id>\d+)/$', views.get_comments, name="get_comments"),


    url(r'^profile/(?P<username>[^/]+)/$',views.profile, name="profile"),

    url(r'^edit_profile/$',views.edit_profile, name="edit_profile"),
    url(r'^profile_pic_url/(?P<username>[^/]+)/$',views.profile_pic_url, name="profile_pic_url"),

    url(r'^scripts/$', views.scripts, name="scripts"),
    
    url(r'^follow/(?P<username>[^/]+)/$', views.follow, name='follow'),
    url(r'^unfollow/(?P<username>[^/]+)/$', views.unfollow, name='unfollow'),

    url(r'^follower_stream/$', views.follower_stream, name="follower_stream"),

)