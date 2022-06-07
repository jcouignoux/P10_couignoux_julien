from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested.routers import NestedSimpleRouter
from knox import views as knox_views

from api.views import ProjectViewset, AdminProjectViewset, ContributorViewset, IssueViewset, CommentViewset, RegisterView, LoginAPI

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

router.register('admin/projects', AdminProjectViewset,
                basename='admin-projects')

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
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
