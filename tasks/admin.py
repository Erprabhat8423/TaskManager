from django.contrib import admin
from .models import Task, Comment

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'created_by')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('status', 'due_date')
    filter_horizontal = ('members',)
    raw_id_fields = ('created_by',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('content', 'author__username', 'task__title')
    list_filter = ('created_at',)
    raw_id_fields = ('task', 'author')

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
