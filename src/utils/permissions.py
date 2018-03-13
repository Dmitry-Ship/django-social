from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user



# class IsFollowerOrReadOnly(permissions.BasePermission):
#     """
#     View-level permission to allow the follower to edit the following relation
#     """
#
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         try:
#             follower = User.objects.get(id=view.kwargs["pk"])
#         except User.DoesNotExist:
#             #Reject any request for an invalid user
#             return False
#
#         return follower == request.user