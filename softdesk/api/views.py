from django.contrib.auth import login, logout
from django.db import transaction

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from api.models import Project, Issue, Comment, Contributor, RoleEnum
from api.serializers import ProjectListSerializer, ProjecDetailSerializer, IssueListSerializer, IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer, ContributorListSerializer, ContributorDetailSerializer, RegisterSerializer, UserListSerializer
from api.permissions import IsAuthenticated
# Create your views here.


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjecDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        contributor = Contributor.objects.filter(user_id=user).all()
        return Project.objects.filter(contributed_by__in=contributor)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        contributor = Contributor.objects.create(
            user_id=request.user,
            project_id=project,
            role=RoleEnum.CREATOR
        )

        return Response({
            'project': ProjectListSerializer(project, context=self.get_serializer_context()).data,
            'message': "Project and Contributor created successfully.",
        })


class AdminProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjecDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['project_id'] = Project.objects.get(
            project_id=self.kwargs['project_pk'])
        serializer.is_valid(raise_exception=True)

        issue = serializer.save(
            author_user_id=request.user, project_id=serializer.context['project_id'])

        return Response({
            'contributor': IssueListSerializer(issue, context=self.get_serializer_context()).data,
            'message': "Contributor added successfully.",
        })


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):

        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):

        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = Project.objects.get(project_id=self.kwargs['project_pk'])
        contributor = serializer.save(project_id=project_id)

        return Response({
            'contributor': ContributorListSerializer(contributor, context=self.get_serializer_context()).data,
            'message': "Contributor added successfully.",
        })


class AdminIssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()


@ permission_classes([AllowAny])
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': RegisterSerializer(user, context=self.get_serializer_context()).data,
            'message': "User created successfully.",
        })
