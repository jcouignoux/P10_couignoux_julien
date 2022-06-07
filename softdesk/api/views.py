from django.contrib.auth import login

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from api.models import Project, Issue, Comment, Contributor
from api.serializers import ProjectListSerializer, ProjecDetailSerializer, UserSerializer, RegisterSerializer, IssueListSerializer, IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer, ContributorListSerializer, ContributorDetailSerializer

# Create your views here.


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjecDetailSerializer

    def get_queryset(self):
        # print(self.request.user)
        return Project.objects.all()


class AdminProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjecDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()


class IssueViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):

        return Issue.objects.filter(project_id=self.kwargs['project_pk'])


class CommentViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):

        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])


class ContributorViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):

        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])


class AdminIssueViewsetViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()


class LoginAPI(KnoxLoginView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return super(LoginAPI, self).post(request, format=None)


class RegisterView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })

        return response
