from django.contrib import admin

from freudiancommits.github import models


class RepoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name')
    search_fields = ('owner', 'name')

admin.site.register(models.Repo, RepoAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('repo', 'number', 'title', 'resolved')
    list_filter = ('resolved',)
    raw_id_fields = ('repo',)

admin.site.register(models.Issue, IssueAdmin)


class StarredRepoAdmin(admin.ModelAdmin):
    list_display = ('account', 'repo')
    raw_id_fields = ('account', 'repo')

admin.site.register(models.StarredRepo, StarredRepoAdmin)
