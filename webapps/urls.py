from django.conf.urls import patterns, include, url
import socialnetwork.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	# url(r'^admin/', include(admin.site.urls)),


    url(r'^', include(socialnetwork.urls))
)
