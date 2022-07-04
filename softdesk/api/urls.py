from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested.routers import NestedSimpleRouter

from api.views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset, RegisterAPIView, LoginAPIView


router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

projects_router = NestedSimpleRouter(router, 'projects', lookup='project')

projects_router.register('users', ContributorViewset,
                         basename='projects-users')

projects_router.register('issues', IssueViewset, basename='projects-issues')

issues_router = NestedSimpleRouter(projects_router, 'issues', lookup='issue')

issues_router.register('comments', CommentViewset,
                       basename='projects-issues-comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='tocken'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
