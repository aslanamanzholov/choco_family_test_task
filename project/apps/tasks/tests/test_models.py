from django.test import TestCase

from tasks.models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        Task.objects.create(name="Task 51232",
                            priority="LOW",
                            end_date="2020-01-01",
                            status="DONE")
        Task.objects.create(name="Task 5123",
                            priority="LOW",
                            end_date="2020-01-01",
                            status="DONE")

    def test_experiment_email(self):
        task_1 = Task.objects.get(username='user_for_test_1')
        task_2 = Task.objects.get(username='user_for_test_2')
        self.assertEqual(
            task_1.name, "Task 51232")
        self.assertEqual(
            task_2.name, "5123")
