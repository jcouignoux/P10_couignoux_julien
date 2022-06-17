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
        contributor = Contributor.objects.filter(
            user_id=request.user.id, project_id=project_id).all()
        if contributor:
            return True

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        obj_class = obj.__class__.__name__
        if obj_class == "Project":
            project = obj
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
            else:
                return False
        elif obj_class == "Comment":
            project = obj.issue_id.project_id
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
            else:
                return False
        else:
            project = obj.project_id
            contributor = Contributor.objects.filter(
                user_id=request.user.id, project_id=project.project_id).first()
            if contributor:
                role = contributor.role
            else:
                return False
        if request.method == "GET":
            if role in ("A", "M", "C"):
                return True
        elif request.method == "PUT":
            if role in ("A", "C"):
                return True
        elif request.method == "DELETE":
            if role in ("A", "C"):
                return True

        return False
