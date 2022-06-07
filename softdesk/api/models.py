from pyexpat import model
from random import choices
from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8192)
    TYPE_CHOICES = (
        ("B", "BackEnd"),
        ("F", "FrontEnd"),
        ("I", "iOS"),
        ("A", "Android")
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title + str(self.project_id)


class Contributor(models.Model):
    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    project_id = models.ForeignKey(
        to=Project, on_delete=models.DO_NOTHING)
    PERM_CHOICES = (
        ("A", "Author"),
        ("M", "Manager"),
        ("C", "Creator")
    )
    permission = models.CharField(max_length=1, choices=PERM_CHOICES)
    role = models.CharField(max_length=128)

    def __str__(self):
        return self.user_id.username


class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=8192)
    TAG_CHOICES = (
        ("B", "Bug"),
        ("I", "Improvement"),
        ("T", "Task")
    )
    tag = models.CharField(max_length=1, choices=TAG_CHOICES)
    PRIORITY_CHOICES = (
        ("H", "Hight"),
        ("M", "Medium"),
        ("L", "Low")
    )
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(
        to=Project, on_delete=models.DO_NOTHING)
    STATUS_CHOICES = (
        ("T", "ToDo"),
        ("I", "InProgress"),
        ("C", "Closed")
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='issue_author')
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='issue_assignee', default=author_user_id)
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
