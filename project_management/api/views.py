from re import M
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Users, Projects, ProjectMembers, Tasks, Comments
from .serializers import (
    RegisterUserSerializer,
    UserSerializer,
    ProjectSerializer,
    ProjectCreateUpdateSerializer,
    ProjectMemberSerializer,
    ProjectMemberCreateSerializer,
    TaskSerializer,
    TaskCreateUpdateSerializer,
    CommentSerializer,
    CommentCreateUpdateSerializer,
)


# Users ViewSet
class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def register(self, request):
        """POST /api/users/register/"""
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        """POST /api/users/login/"""
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = Users.objects.get(email=email)
            if not user.check_password(password):
                raise ValueError("Invalid credentials")
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        except Users.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """GET /api/users/{id}/"""
        user = Users.objects.filter(pk=pk).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        PUT: Full update of a user.
        """
        user = Users.objects.filter(pk=pk).first()
        if not user:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RegisterUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        PATCH: Partial update of a user.
        """
        user = Users.objects.filter(pk=pk).first()
        if not user:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RegisterUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """DELETE /api/users/{id}/"""
        user = Users.objects.filter(pk=pk).first()
        if user:
            user.delete()
            return Response(
                {"detail": "User deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Projects ViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Projects.
    Supports list, create, retrieve, update, and delete.
    """

    queryset = Projects.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Dynamically choose the serializer:
        - Use `ProjectSerializer` for read operations (list, retrieve).
        - Use `ProjectCreateUpdateSerializer` for write operations (create, update, partial_update).
        """
        if self.action in ["create", "update", "partial_update"]:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        """
        Automatically set the authenticated user as the owner.
        """
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override POST to use `ProjectCreateUpdateSerializer` for validation
        and `ProjectSerializer` for the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Format response with ProjectSerializer
        output_serializer = ProjectSerializer(
            serializer.instance, context={"request": request}
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Override PUT for full updates.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Format response with ProjectSerializer
        output_serializer = ProjectSerializer(instance, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Override PATCH for partial updates.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Format response with ProjectSerializer
        output_serializer = ProjectSerializer(instance, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

class ProjectMemberViewSet(viewsets.ViewSet):
    """
    ViewSet for managing Project Members.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request, project_id=None):
        """GET /api/projects/{project_id}/members/"""
        members = ProjectMembers.objects.filter(project_id=project_id)
        serializer = ProjectMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, project_id=None):
        """POST /api/projects/{project_id}/members/"""
        serializer = ProjectMemberCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """GET /api/members/{id}/"""
        member = ProjectMembers.objects.filter(pk=pk).first()
        if member:
            serializer = ProjectMemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Member not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def update(self, request, pk=None):
        """PUT /api/members/{id}/"""
        member = ProjectMembers.objects.filter(pk=pk).first()
        if member:
            serializer = ProjectMemberCreateSerializer(
                member, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "Member not found"}, status=status.HTTP_404_NOT_FOUND
        )
    
    def partial_update(self, request, pk=None):
        """
        PATCH /api/members/{id}/
        """
        member = ProjectMembers().objects.filter(pk=pk).first()
        if not member:
            return Response({"detail": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectMemberCreateSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """DELETE /api/members/{id}/"""
        member = ProjectMembers.objects.filter(pk=pk).first()
        if member:
            member.delete()
            return Response(
                {"detail": "Member deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "Member not found"}, status=status.HTTP_404_NOT_FOUND
        )

# Task ViewSet
class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, project_id=None):
        """GET /api/projects/{project_id}/tasks/"""
        tasks = Tasks.objects.filter(project_id=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, project_id=None):
        """
        POST /api/projects/{project_id}/tasks/
        """
        data = request.data.copy()  # Create a mutable copy of the request data
        data["project"] = project_id  # Set the project field from the URL parameter
        serializer = TaskCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """GET /api/tasks/{id}/"""
        task = Tasks.objects.filter(pk=pk).first()
        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """PUT /api/tasks/{id}/"""
        task = Tasks.objects.filter(pk=pk).first()
        if task:
            serializer = TaskCreateUpdateSerializer(
                task, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        """
        PATCH /api/tasks/{id}/
        """
        task = Tasks.objects.filter(pk=pk).first()
        if not task:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskCreateUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """DELETE /api/tasks/{id}/"""
        task = Tasks.objects.filter(pk=pk).first()
        if task:
            task.delete()
            return Response(
                {"detail": "Task deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


# Comments ViewSet
class CommentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, task_id=None):
        """GET /api/tasks/{task_id}/comments/"""
        comments = Comments.objects.filter(task_id=task_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, task_id=None):
        """
        POST /api/tasks/{task_id}/comments/
        """
        data = request.data.copy()  # Create a mutable copy of the request data
        data["user"] = request.user.id  # Set the user to the authenticated user
        data["task"] = task_id  # Set the task to the task_id from the URL
        serializer = CommentCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """GET /api/comments/{id}/"""
        comment = Comments.objects.filter(pk=pk).first()
        if comment:
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def update(self, request, pk=None):
        """PUT /api/comments/{id}/"""
        comment = Comments.objects.filter(pk=pk).first()
        if comment:
            serializer = CommentCreateUpdateSerializer(
                comment, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def destroy(self, request, pk=None):
        """DELETE /api/comments/{id}/"""
        comment = Comments.objects.filter(pk=pk).first()
        if comment:
            comment.delete()
            return Response(
                {"detail": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )
