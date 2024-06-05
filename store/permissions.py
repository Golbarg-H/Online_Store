from rest_framework import permissions


class UpdateOrderPermission(permissions.BasePermission):
    message = 'Updating an order is not allowed.'

    def has_permission(self, request, view):
        if request.method not in ['PUT', 'PATCH']:
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Updating an product is not allowed.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.add_%(model_name)s']


class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perms(['store.view_history'])
