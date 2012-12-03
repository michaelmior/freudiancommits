from django.db import models

from allauth.socialaccount.models import SocialAccount


class Repo(models.Model):
    owner = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    pushed_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __unicode__(self):
        return '%s/%s' % (self.owner, self.name)

    def get_absolute_url(self):
        return 'https://github.com/%s' % unicode(self)

    class Meta:
        ordering = ('owner', 'name')
        verbose_name = 'repository'
        verbose_name_plural = 'repositories'


class Issue(models.Model):
    repo = models.ForeignKey(Repo, related_name='issues')
    number = models.IntegerField(
            verbose_name='issue number')
    assignee = models.CharField(max_length=100, null=True, default=None)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    resolved = models.BooleanField(default=False)
    title = models.CharField(max_length=500)
    body = models.TextField()

    def __unicode__(self):
        return '%s#%d' % (unicode(self.repo), self.number)

    def get_absolute_url(self):
        return 'https://github.com/%s/%s/issues/%d' % \
                (self.repo.owner, self.repo.name, self.number)

    class Meta:
        get_latest_by = 'updated_at'
        ordering = ('repo__owner', 'repo__name', 'number')
        unique_together = ('repo', 'number')


class StarredRepo(models.Model):
    account = models.ForeignKey(SocialAccount, related_name='starred_repos')
    repo = models.ForeignKey(Repo)

    class Meta:
        ordering = ('account__user__username', 'repo__owner', 'repo__name')
        unique_together = ('account', 'repo')
        verbose_name = 'starred repository'
        verbose_name_plural = 'starred repositories'
