from django.conf.urls import patterns, url
from freudiancommits.github import views


urlpatterns = patterns('',
    url(r'^fetch_data/$', views.FetchDataView.as_view()),
    url(r'^issue/(?P<issue_id>\d+)/$', views.IssueView.as_view()),
)
