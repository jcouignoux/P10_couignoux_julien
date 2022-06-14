from django_enum_choices.fields import EnumChoiceField
from enum import Enum, unique
from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=8192)
    TYPE_CHOICES = (
        ("B", "BackEnd"),
        ("F", "FrontEnd"),
        ("I", "iOS"),
        ("A", "Android")
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title


@unique
class RoleEnum(Enum):
    AUTHOR = 'Author'
    MANAGER = 'Manager'
    CREATOR = 'Creator'

    @classmethod
    def choices(cls):
        return [(i, i.value) for i in cls]


class Contributor(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='contributing', limit_choices_to={'is_staff': False})
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE,
                                   related_name='contributed_by')
    ROLE_CHOICES = (
        ("A", "Author"),
        ("M", "Manager"),
        ("C", "Creator")
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default="M")

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
        to=Project, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("T", "ToDo"),
        ("I", "InProgress"),
        ("C", "Closed")
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='issue_author', limit_choices_to={'is_staff': False})
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='issue_assignee', limit_choices_to={'is_staff': False})
    #  related_name='issue_assignee', limit_choices_to=Contributor.objects.filter(project_id=project_id))
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # def assignee_limit_choice(self):
        # assignees = [(Contributor.object) for Contribut]
        # return assignees


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=8192)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})
    issue_id = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment_id) + str(self.description)
