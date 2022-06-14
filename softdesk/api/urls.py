from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested.routers import NestedSimpleRouter

# , RegisterView, LoginAPI
from api.views import ProjectViewset, AdminProjectViewset, ContributorViewset, IssueViewset, CommentViewset, RegisterAPI

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

projects_router = NestedSimpleRouter(router, 'projects', lookup='project')

projects_router.register('users', ContributorViewset,
                         basename='projects-users')

projects_router.register('issues', IssueViewset, basename='projects-issues')

issues_router = NestedSimpleRouter(projects_router, 'issues', lookup='issue')

issues_router.register('comments', CommentViewset,
                       basename='projects-issues-comments')

router.register('admin/projects', AdminProjectViewset,
                basename='admin-projects')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
    path('signup/', RegisterAPI.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
