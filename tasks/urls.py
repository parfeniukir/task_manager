from django.urls import path

from .views import TaskListView, TaskCreateView

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
]
