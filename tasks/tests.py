from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Task
from .forms import TaskForm

User = get_user_model()


class TaskViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user1", password="pass12345")
        cls.user2 = User.objects.create_user(username="user2", password="pass12345")

        cls.task_user1 = Task.objects.create(
            title="User 1 task",
            description="Desc 1",
            deadline=date.today() + timedelta(days=7),
            owner=cls.user1,
        )
        cls.task_user2 = Task.objects.create(
            title="User 2 task",
            description="Desc 2",
            deadline=date.today() + timedelta(days=5),
            owner=cls.user2,
        )

    def test_task_list_requires_login(self):
        url = reverse("task-list")
        responce = self.client.get(url)
        print()

        self.assertEqual(responce.status_code, 302)
        self.assertIn("/accounts/login/", responce["Location"])

    def test_task_list_shows_only_own_tasks(self):
        self.client.login(username="user1", password="pass12345")

        url = reverse("task-list")
        responce = self.client.get(url)

        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, "User 1 task")
        self.assertNotContains(responce, "User 2 task")

    def test_create_task_sets_owner_automatically(self):
        self.client.login(username="user1", password="pass12345")

        url = reverse("task-create")
        payload = {
            "title": "New task",
            "description": "Some text",
            "deadline": date.today() + timedelta(days=7),
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 302)

        created = Task.objects.get(title="New task")
        self.assertEqual(created.owner, self.user1)

    def test_toggle_complete_changes_status(self):
        self.client.login(username="user1", password="pass12345")

        url = reverse("task-toggle", kwargs={"pk": self.task_user1.pk})
        self.assertFalse(Task.objects.get(pk=self.task_user1.pk).is_completed)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Task.objects.get(pk=self.task_user1.pk).is_completed)

    def test_toggle_complete_forbidden_for_other_users_task(self):
        self.client.login(username="user1", password="pass12345")

        url = reverse("task-toggle", kwargs={"pk": self.task_user2.pk})
        response = self.client.post(url)

        # UserPassesTestMixin зазвичай дає 403
        self.assertIn(response.status_code, [403, 404])

        # Статус чужої задачі не змінюється
        self.assertFalse(Task.objects.get(pk=self.task_user2.pk).is_completed)


class TaskFormTests(TestCase):
    def test_deadline_cannot_be_in_past(self):
        form = TaskForm(
            data={
                "title": "T",
                "description": "D",
                "deadline": date.today() - timedelta(days=1),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_deadline_can_be_today_or_future(self):
        form = TaskForm(
            data={
                "title": "T",
                "description": "D",
                "deadline": date.today(),
            }
        )
        self.assertTrue(form.is_valid())
