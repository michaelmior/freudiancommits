import urllib2

from django.views.generic.base import TemplateView, View
from django import http
from django.shortcuts import get_object_or_404

from allauth.socialaccount.models import SocialAccount, SocialToken
import sanction.client

from freudiancommits.github import models


class FetchDataView(View):

    def get_account(self, user):
        """
        Try to find a GitHub account for the given user
        """
        try:
            account = user.socialaccount_set \
                    .get(provider='github')
        except (SocialAccount.DoesNotExist, \
                SocialAccount.MultipleObjectsReturned):
            return None

        return account

    def get_client(self, account):
        """
        Get a sanction client for the given account
        if the access token exists in the database
        """
        if not account:
            return None

        try:
            token = account.socialtoken_set.get().token
        except SocialToken.DoesNotExist:
            return None

        client = sanction.client.Client(
                resource_endpoint='https://api.github.com/')
        client.access_token = token

        return client

    def fetch_repo_issues(self, client, repo):
        try:
            issues = client.request('repos/%s/%s/issues' % \
                    (repo.owner, repo.name))
        except urllib2.HTTPError:
            return

        for issue in issues:
            # Skip existing issues
            if models.Issue.objects.filter(
                    repo=repo,
                    number=issue['number']).exists():
                continue

            db_issue = models.Issue(repo=repo)

            for field in ('number', 'created_at', 'updated_at',
                    'title', 'body'):
                setattr(db_issue, field, issue[field])

            db_issue.assignee = (issue.get('assignee') or {}).get('login')
            db_issue.resolved = issue['state'] == 'closed'

            # Only save unresolved issues
            if not db_issue.resolved:
                db_issue.save()

    def fetch_repos(self, account, client):
        for repo in client.request('user/starred'):

            # Assume if repo exists that all data has been fetched
            if models.Repo.objects.filter(
                    owner=repo['owner']['login'],
                    name=repo['name']).exists():
                continue

            db_repo = models.Repo(
                    owner=repo['owner']['login'],
                    name=repo['name'])

            for field in ('pushed_at', 'created_at', 'updated_at'):
                setattr(db_repo, field, repo[field])

            db_repo.save()
            models.StarredRepo(account=account, repo=db_repo).save()

            self.fetch_repo_issues(client, db_repo)

    def get(self, request, *args, **kwargs):
        # Try to get an account and client for access
        account = self.get_account(request.user)
        client = self.get_client(account)
        if not account or not client:
            return http.HttpResponseBadRequest()

        # Quit if we already have starred repos for the user
        if account.starred_repos.exists():
            return http.HttpResponse()

        self.fetch_repos(account, client)

        return http.HttpResponse()


class IssueView(TemplateView):
    template_name = 'issue.html'

    def get_context_data(self, **kwargs):
        context = super(IssueView, self).get_context_data(**kwargs)
        context['issue'] = get_object_or_404(models.Issue,
                pk=kwargs['issue_id'])
        return context


class RandomIssueView(TemplateView):
    template_name = 'randomissue.json'

    def get_context_data(self, **kwargs):
        context = super(RandomIssueView, self).get_context_data(**kwargs)
        context['issue'] = models.Issue.objects.filter(
                repo__starredrepo__account__user=self.request.user) \
                        .order_by('?')[0]
        return context

    def get(self, request, *args, **kwargs):
        response = super(RandomIssueView, self).get(request, *args, **kwargs)
        response['Content-Type'] = 'application/json'
        return response


class LoadingView(TemplateView):
    template_name = 'loading.html'
