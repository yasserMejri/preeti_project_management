from django.conf.urls import url
from coordinator import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^projects/$', views.projects, name="projects"), 
    url(r'^project/(?P<p_id>\d+)/$', views.project, name="project")
]
