from django.contrib.auth import logout, authenticate
from django.db import IntegrityError, transaction

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.mixins import UpdateModelMixin

from api.models import Project, Issue, Comment, Contributor
from api.serializers import (ProjectListSerializer,
                             ProjecDetailSerializer,
                             IssueListSerializer,
                             IssueDetailSerializer,
                             CommentListSerializer,
                             CommentDetailSerializer,
                             ContributorListSerializer,
                             ContributorDetailSerializer,
                             RegisterSerializer,
                             LoginSerializer)
from api.permissions import AuthorOrReadOnly
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
    permission_classes = [AuthorOrReadOnly]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

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
            role="C"
        )

        return Response({
            'project': ProjectListSerializer(project, context=self.get_serializer_context()).data,
            'message': "Project and Contributor created successfully."},
            status=status.HTTP_201_CREATED)


class IssueViewset(MultipleSerializerMixin, ModelViewSet, UpdateModelMixin):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [AuthorOrReadOnly]

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
            'message': "Issue created successfully."},
            status=status.HTTP_201_CREATED)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):

        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['issue_id'] = Issue.objects.get(
            issue_id=self.kwargs['issue_pk'])
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(
            author_user_id=request.user, issue_id=serializer.context['issue_id'])

        return Response({
            'contributor': CommentListSerializer(comment, context=self.get_serializer_context()).data,
            'message': "Comment created successfully."},
            status=status.HTTP_201_CREATED)


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):

        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = Project.objects.get(project_id=self.kwargs['project_pk'])
        try:
            cont = serializer.save(project_id=project_id)
            contributor = ContributorListSerializer(
                cont, context=self.get_serializer_context()).data
            message = "Contributor added successfully."
        except IntegrityError:
            contributor = ''
            message = "User already contributor of project."

        return Response({
            'contributor': contributor,
            'message': message},
            status=status.HTTP_201_CREATED)


class AdminIssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [AuthorOrReadOnly]
    queryset = Issue.objects.all()


@ permission_classes([AllowAny])
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': RegisterSerializer(user, context=self.get_serializer_context()).data,
                'message': "User created successfully."},
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)

        if user:
            serializer = self.serializer_class(user)

            return Response({
                'message': "User logged successfully.",
            },
                status=status.HTTP_200_OK
            )

        return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
