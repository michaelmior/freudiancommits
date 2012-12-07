from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from freudiancommits.github import views


urlpatterns = patterns('',
    url(r'^fetch_data/$', views.FetchDataView.as_view()),
    url(r'^issue/(?P<issue_id>\d+)/$', views.IssueView.as_view()),
    url(r'^randomissue/$', login_required(views.RandomIssueView.as_view())),
)
