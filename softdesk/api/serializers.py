from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Project, Issue, Comment, Contributor


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'description', 'created_time']
        read_only_fields = ['comment_id', 'author_user_id', 'issue_id']


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'description',
                  'author_user_id', 'issue_id', 'created_time']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'desc',
                  'tag', 'priority', 'status', 'assignee_user_id', 'created_time']
        read_only_fields = ['project_id', 'author_user_id']


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'desc', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'assignee_user_id', 'created_time', 'comments']
        read_only_fields = ['project_id']

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type']


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
        fields = ['id', 'user_id', 'project_id', 'role']
        read_only_fields = ['project_id']


class ContributorDetailSerializer(ModelSerializer):

    user = SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id', 'role', 'user']

    def get_user(self, instance):
        queryset = User.objects.get(id=instance.user_id.id)
        serializer = UserDetailSerializer(queryset, many=False)
        return serializer.data


class TokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name']
                                        )
        return user


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class LoginSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']
