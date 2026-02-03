from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import redirect

from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task-list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskToggleCompleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        task = Task.objects.filter(pk=self.kwargs["pk"]).first()
        return task is not None and task.owner == self.request.user

    def post(self, request, *agrs, **kwargs):
        task = Task.objects.get(pk=kwargs["pk"], owner=request.user)
        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed"])
        return redirect("task-list")


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = "tasks/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("task-list")

    def test_func(self):
        task = self.get_object()
        return task.owner == self.request.user


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")

    def test_func(self):
        task = self.get_object()
        return task.owner == self.request.user
