from django.conf.urls import url
from coordinator import views
from coordinator import project_views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^projects/$', views.projects, name="projects"), 
    url(r'^project/(?P<p_id>\d+)/$', views.project, name="project"), 
    url(r'^project/(?P<p_id>\d+)/data-sources', project_views.data_sources_project, name="data-sources"), 
    url(r'^project/(?P<p_id>\d+)/preview/$', project_views.preview_project, name="preview"), 
    url(r'^project/(?P<p_id>\d+)/preview_post/$', project_views.preview_post_project, name="preview_post"), 
    url(r'^project/(?P<p_id>\d+)/experiments', project_views.experiments_project, name="experiments"), 
    url(r'^project/(?P<p_id>\d+)/results', project_views.results_project, name="results"), 
    url(r'^project/(?P<p_id>\d+)/predict', project_views.predict_project, name="predict"), 
    url(r'^project/(?P<p_id>\d+)/feature', project_views.feature_project, name="feature"), 
    url(r'^project/(?P<p_id>\d+)/deploy', project_views.deploy_project, name="deploy"), 
    url(r'^project/(?P<p_id>\d+)/api_status', project_views.api_project, name="api_status"), 
]
