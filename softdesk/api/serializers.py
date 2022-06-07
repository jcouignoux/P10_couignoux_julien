from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError

from api.models import Project, Issue, Comment, Contributor


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['description']


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'description',
                  'author_user_id', 'issue_id', 'created_time']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'status']


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'desc', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'assignee_user_id', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title',
                  'description', 'type']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError('Project title already exists')
        return value


class ProjecDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'issues']

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project_id=instance)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user_id', 'role']


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id',
                  'permission', 'role']


class TokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['password'])

        return user
