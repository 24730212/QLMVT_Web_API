from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Người dùng phải đăng nhập.
    """

    message = "Bạn cần đăng nhập để thực hiện thao tác này."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(BasePermission):
    """
    Chỉ Admin được phép.
    """

    message = "Bạn không có quyền Admin."

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )


class IsUser(BasePermission):
    """
    Chỉ User thường.
    """

    message = "Chỉ User mới được phép thực hiện thao tác này."

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and not request.user.is_staff
        )


class IsAdminOrReadOnly(BasePermission):
    """
    User:
        GET / HEAD / OPTIONS

    Admin:
        GET / POST / PUT / PATCH / DELETE
    """

    message = "Bạn không có quyền thay đổi dữ liệu."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        return request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
    Admin:
        được thao tác mọi object.

    User:
        chỉ được thao tác object của chính mình.

    View phải có:
        get_object_owner(obj)
    """

    message = "Bạn chỉ được phép thao tác dữ liệu của chính mình."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        owner = view.get_object_owner(obj)

        return owner == request.user


class IsAssignedEmployeeOrAdmin(BasePermission):
    """
    Admin:
        được thao tác mọi lỗi/lỗ hổng.

    User:
        chỉ được thao tác lỗi/lỗ hổng
        mà mình được phân công.

    View phải có:
        get_assigned_employee(obj)

    get_assigned_employee(obj)
    phải trả về NhanVien.
    """

    message = "Bạn không phải nhân viên được phân công " "xử lý dữ liệu này."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        assigned_employee = view.get_assigned_employee(obj)

        if assigned_employee is None:
            return False

        try:
            account = request.user.employee_account
        except Exception:
            return False

        return account.nhan_vien.ma_nv == assigned_employee.ma_nv
