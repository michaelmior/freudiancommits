from django.conf.urls import patterns, url
from freudiancommits.github import views


urlpatterns = patterns('',
    url(r'^fetch_data/$', views.FetchDataView.as_view()),
)
