from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ProjectViewSet,
    ProjectMemberViewSet,
    TaskViewSet,
    CommentViewSet,
)

# Router setup
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(
    r"projects/(?P<project_id>[^/.]+)/members",
    ProjectMemberViewSet,
    basename="project-members",
)
router.register(r"members", ProjectMemberViewSet, basename="members")
router.register(r"tasks", TaskViewSet, basename="tasks")  # Add TaskViewSet
router.register(r"comments", CommentViewSet, basename="comments")  # Add CommentViewSet

# URL patterns
urlpatterns = [
    path("api/", include(router.urls)),
    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Nested endpoints for tasks and comments
    path(
        "api/projects/<int:project_id>/tasks/",
        TaskViewSet.as_view({"get": "list", "post": "create"}),
        name="project-tasks",
    ),
    path(
        "api/tasks/<int:pk>/",
        TaskViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="task-detail",
    ),
    path(
        "api/tasks/<int:task_id>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="task-comments",
    ),
    path(
        "api/comments/<int:pk>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comment-detail",
    ),
    
]
