from rest_framework.permissions import BasePermission

from api.models import Project, Contributor


class AuthorOrReadOnly(BasePermission):

    edit_methods = ("GET", "PUT", "DELETE")

    def has_permission(self, request, view):
        if view.kwargs.get('project_pk'):
            pk = view.kwargs['project_pk']
        elif view.kwargs.get('pk'):
            pk = view.kwargs['pk']
        else:
            pk = 0
        project_id = Project.objects.filter(project_id=pk).first()
        if project_id != None:
            cont = Contributor.objects.filter(
                user_id=request.user.id, project_id=project_id).first()
            if cont != None:
                contributor = True
            else:
                contributor = False
        else:
            contributor = True

        return bool(request.user and request.user.is_authenticated) and contributor

    def has_object_permission(self, request, view, obj):
        obj_class = obj.__class__.__name__
        author = False
        if obj_class == "Project":
            project = obj
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
            if role == "C":
                author = True
        elif obj_class == "Issue":
            project = obj.project_id
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
            if obj.author_user_id == request.user:
                author = True
        elif obj_class == "Comment":
            project = obj.issue_id.project_id
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
            if obj.author_user_id.id == request.user.id:
                author = True
        elif obj_class == "Contributor":
            project = obj.project_id
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
            if role == "C":
                author = True
        else:
            project = obj.project_id
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
        if request.method == "GET":
            if role in ("A", "M", "C"):
                return True
        elif request.method == "PUT" or request.method == "DELETE":
            if author:
                return True

        return False
