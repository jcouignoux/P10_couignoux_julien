from django.contrib import admin


from api.models import Project, Contributor, Issue, Comment
# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['project_id', 'title', 'description', 'type']


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    search_fields = ['user_id', 'project_id', 'permission', 'role']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ['title', 'desc', 'tag', 'priority', 'project_id',
                     'status', 'author_user_id', 'assignee_user_id', 'created_time']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['comment_id', 'description',
                     'author_user_id', 'issue_id', 'created_time']
