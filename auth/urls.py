from django.conf.urls import url
import views

urlpatterns = [
    url(r'login/$', views.auth_login, name="login"),
    url(r'logout/$', views.auth_logout, name="logout"), 
    url(r'register/$', views.auth_register, name="register"), 
    url(r'profile/$', views.auth_profile, name="profile")
]
