from django.urls import path

from .views import (TaskCreateView, TaskDeleteView, TaskListView,
                    TaskToggleCompleteView, TaskUpdateView, TaskDetailView)

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/toggle/", TaskToggleCompleteView.as_view(), name="task-toggle"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("<int:pk>/detail/", TaskDetailView.as_view(), name="task-detail"),
]
