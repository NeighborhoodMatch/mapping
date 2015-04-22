from django.conf.urls import patterns, url
from nmatch import views

urlpatterns = patterns('', 

	#/nmatch/home/
	url(r'^home/$', views.home, name='home'),
	#/nmatch/about/
	url(r'^about/$', views.about, name='about'),
	#/nmatch/survey/
	url(r'^survey/$', views.survey_CAPP, name='survey'),
	#/nmatch/onlymap/
	#url(r'^onlymap/$', views.survey, name='onlymap')
)