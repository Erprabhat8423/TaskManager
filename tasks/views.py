from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Task, Comment
from django.contrib.auth import authenticate
from .serializers import TaskSerializer, CommentSerializer, UserRegisterSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            title="User Registration",
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username of the user."),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="The email address of the user."),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="The password for the user.")
            },
            required=['username', 'email', 'password']
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                examples={
                    "application/json": {
                        "username": "newuser",
                        "token": "your-token"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "username": ["This field is required."],
                        "email": ["This field is required."],
                        "password": ["This field is required."]
                    }
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        try:
            user = User.objects.get(username=response.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            response.data['token'] = token.key
        except User.DoesNotExist:
            response.data['token'] = 'User not found after registration.'
        return response
        response = super().create(request, *args, **kwargs)
        try:
            user = User.objects.get(username=response.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            response.data['token'] = token.key
        except User.DoesNotExist:
            response.data['token'] = 'User not found after registration.'
        return response
    
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful.",
                examples={
                    "application/json": {
                        "token": "your-token"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials.",
                examples={
                    "application/json": {
                        "error": "Invalid Credentials"
                    }
                }
            )
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        request_body=TaskSerializer,
        responses={
            201: openapi.Response(
                description="Task created successfully.",
                examples={
                    "application/json": {
                        "id": 1,
                        "name": "Task name",
                        "description": "Task description",
                        "created_by": "username",
                        "status": "todo",
                        "message": "Task created successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error.",
                examples={
                    "application/json": {
                        "name": ["This field is required."],
                        "description": ["This field is required."]
                    }
                }
            )
        }
    )
    def perform_create(self, serializer):
        try:
            serializer.save(created_by=self.request.user)
        except Exception as e:
            raise ValidationError({"detail": str(e)})

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data['message'] = 'Task created successfully.'
            return response
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of tasks with comments.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "name": "Task 1",
                            "description": "Description of Task 1",
                            "created_by": "username",
                            "status": "todo",
                            "comments": [
                                {
                                    "id": 1,
                                    "text": "Comment text",
                                    "author": "comment_author",
                                    "created_at": "2024-01-01T00:00:00Z"
                                }
                            ]
                        },
                        {
                            "id": 2,
                            "name": "Task 2",
                            "description": "Description of Task 2",
                            "created_by": "username",
                            "status": "inprogress",
                            "comments": []
                        }
                    ]
                }
            ),
            500: openapi.Response(
                description="Internal Server Error.",
                examples={
                    "application/json": {
                        "detail": "An unexpected error occurred."
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve all tasks
            tasks = self.get_queryset()

            # Manually construct the response data to include comments
            response_data = []
            for task in tasks:
                # Serialize the task
                task_data = TaskSerializer(task).data

                # Get related comments
                comments = Comment.objects.filter(task=task)
                comment_data = CommentSerializer(comments, many=True).data

                # Add comments to the task data
                task_data['comments'] = comment_data

                response_data.append(task_data)

            return Response(response_data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Task detail.",
                examples={
                    "application/json": {
                        "id": 1,
                        "name": "Task name",
                        "description": "Task description",
                        "created_by": "username",
                        "status": "todo"
                    }
                }
            ),
            404: openapi.Response(
                description="Task not found.",
                examples={
                    "application/json": {
                        "detail": "Task not found."
                    }
                }
            ),
            500: openapi.Response(
                description="Internal Server Error.",
                examples={
                    "application/json": {
                        "detail": "An unexpected error occurred."
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AddRemoveTaskMemberView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['user_id']
        ),
        responses={
            204: openapi.Response(
                description="User added to task successfully."
            ),
            400: openapi.Response(
                description="Bad Request.",
                examples={
                    "application/json": {
                        "error": "user_id is required"
                    }
                }
            ),
            404: openapi.Response(
                description="Task or User not found.",
                examples={
                    "application/json": {
                        "error": "Task not found"  # or "User not found"
                    }
                }
            )
        }
    )
    def post(self, request, pk):
        try:
            user_id = request.data['user_id']
            task = Task.objects.get(pk=pk)
            user = User.objects.get(id=user_id)
            task.members.add(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['user_id']
        ),
        responses={
            204: openapi.Response(
                description="User removed from task successfully."
            ),
            400: openapi.Response(
                description="Bad Request.",
                examples={
                    "application/json": {
                        "error": "user_id is required"
                    }
                }
            ),
            404: openapi.Response(
                description="Task or User not found.",
                examples={
                    "application/json": {
                        "error": "Task not found"  # or "User not found"
                    }
                }
            )
        }
    )
    def delete(self, request, pk):
        try:
            user_id = request.data['user_id']
            task = Task.objects.get(pk=pk)
            user = User.objects.get(id=user_id)
            task.members.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class TaskMemberListView(generics.ListAPIView):
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of task members.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "username": "user1",
                            "email": "user1@example.com"
                        },
                        {
                            "id": 2,
                            "username": "user2",
                            "email": "user2@example.com"
                        }
                    ]
                }
            ),
            404: openapi.Response(
                description="Task not found.",
                examples={
                    "application/json": {
                        "detail": "Task not found."
                    }
                }
            )
        }
    )
    def get_queryset(self):
        try:
            task = Task.objects.get(pk=self.kwargs['pk'])
            return task.members.all()
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found.")

    def get(self, request, *args, **kwargs):
        try:
            response = super().get(request, *args, **kwargs)
            return response
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={
            201: openapi.Response(
                description="Comment created successfully.",
                examples={
                    "application/json": {
                        "id": 1,
                        "task": 1,
                        "author": "username",
                        "content": "Comment content"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error.",
                examples={
                    "application/json": {
                        "content": ["This field is required."]
                    }
                }
            )
        }
    )
    def perform_create(self, serializer):
        try:
            task = Task.objects.get(pk=self.kwargs['task_pk'])
            serializer.save(task=task, author=self.request.user)
        except Task.DoesNotExist:
            raise serializers.ValidationError({"task": "Task not found."})

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskStatusUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['todo', 'inprogress', 'done'])
            },
            required=['status']
        ),
        responses={
            200: openapi.Response(
                description="Task status updated successfully.",
                examples={
                    "application/json": {
                        "id": 1,
                        "name": "Task name",
                        "description": "Task description",
                        "created_by": "username",
                        "status": "done"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid status value.",
                examples={
                    "application/json": {
                        "status": "Invalid status value. Only 'todo', 'inprogress', or 'done' are allowed."
                    }
                }
            ),
            404: openapi.Response(
                description="Task not found.",
                examples={
                    "application/json": {
                        "detail": "Task not found."
                    }
                }
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            status_value = request.data.get('status')
            
            if status_value not in dict(Task.STATUS_CHOICES).keys():
                return Response({"status": "Invalid status value. Only 'todo', 'inprogress', or 'done' are allowed."}, status=status.HTTP_400_BAD_REQUEST)
            
            task.status = status_value
            task.save()
            
            return Response(TaskSerializer(task).data)
        
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
