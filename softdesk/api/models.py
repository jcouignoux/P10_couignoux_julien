from pyexpat import model
from random import choices
from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8192)
    type = models.CharField(max_length=128)

    def __str__(self):
        return self.title + str(self.project_id)


class Contributor(models.Model):
    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    project_id = models.ForeignKey(
        to=Project, on_delete=models.DO_NOTHING)
    PERM_CHOICES = (
        ("C", "POST"),
        ("R", "GET"),
        ("U", "PUT"),
        ("D", "DELETE")
    )
    permission = models.CharField(max_length=1, choices=PERM_CHOICES)
    role = models.CharField(max_length=128)

    def __str__(self):
        return self.user_id.username


class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=8192)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project_id = models.ForeignKey(
        to=Project, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='issue_author')
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='issue_assignee')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=8192)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    issue_id = models.ForeignKey(
        to=Issue, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment_id) + str(self.description)
