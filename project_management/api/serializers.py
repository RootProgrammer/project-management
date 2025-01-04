from rest_framework import serializers
from .models import Users, Projects, ProjectMembers, Tasks, Comments


# User Serializers
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ["id", "username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]


# Project Serializers
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Projects
        fields = ["id", "name", "description", "owner", "created_at"]


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ["name", "description"]


# Project Member Serializers
class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectMembers
        fields = ["id", "project", "user", "role"]

# Project Member Create Serializers
class ProjectMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMembers
        fields = ["project", "user", "role"]

    def validate_role(self, value):
        """
        Ensure the role is either 'Admin' or 'Member'.
        """
        allowed_roles = ["Admin", "Member"]
        if value not in allowed_roles:
            raise serializers.ValidationError(
                f"Invalid role. Allowed values are: {', '.join(allowed_roles)}"
            )
        return value

    def create(self, validated_data):
        """
        Assign a default role if not provided and save the instance.
        """
        if "role" not in validated_data or not validated_data["role"]:
            validated_data["role"] = "Member"  # Default role is 'Member'
        return super().create(validated_data)

# Task Serializers
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assigned_to",
            "project",
            "created_at",
            "due_date",
        ]


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assigned_to",
            "project",
            "due_date",
        ]


# Comment Serializers
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    task = serializers.PrimaryKeyRelatedField(queryset=Tasks.objects.all())

    class Meta:
        model = Comments
        fields = ["id", "content", "user", "task", "created_at"]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "content", "user", "task", "created_at"]
