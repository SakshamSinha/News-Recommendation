from django.conf.urls import url
from application import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]