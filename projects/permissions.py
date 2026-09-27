from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProjectOwnerOrReadOnly(BasePermission):
    message = "Faqat project egasi bu amalni bajara oladi."
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner_id == request.user.id