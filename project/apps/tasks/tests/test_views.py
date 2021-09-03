import json

from django.test import TestCase, Client

from rest_framework import status

from tasks.models import Task
from tasks.serializers import TaskSerializer

client = Client()


class GetAllTasksTest(TestCase):
    def setUp(self):
        Task.objects.create(name="Task 51231",
                            priority="LOW",
                            end_date="2020-01-01",
                            status="DONE")
        Task.objects.create(name="Task 5122",
                            priority="LOW",
                            end_date="2020-01-01",
                            status="DONE")
        Task.objects.create(name="Task 5123234412",
                            priority="LOW",
                            end_date="2020-01-01",
                            status="DONE")
        Task.objects.create(name="Task 5123123",
                            priority="LOW",
                            end_date="2020-01-01",
                            status="DONE")

    def test_get_all_experiments(self):
        response = client.get('tasks')
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetRetrieveTaskTest(TestCase):
    def setUp(self):
        self.task_1 = Task.objects.create(name="Task 51231232",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")
        self.task_2 = Task.objects.create(name="Task 5123122323",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")
        self.task_3 = Task.objects.create(name="Task 51231223",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")
        self.task_4 = Task.objects.create(name="Task 51231223",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")

    def test_get_valid_single_experiment(self):
        response = client.get('tasks', kwargs={'pk': self.task_2.pk})
        task = Task.objects.get(pk=self.task_2.pk)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_experiment(self):
        response = client.get('tasks', kwargs={'pk': self.task_2.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewTaskTest(TestCase):
    def setUp(self):
        self.valid_payload = {"name": "Task 5123122323",
                              "priority": "LOW",
                              "end_date": "2020-01-01",
                              "status": "DONE"
                              }
        self.invalid_payload = {"name": "",
                                "priority": "LOW",
                                "end_date": "",
                                "status": "DONE"
                                }

    def test_create_valid_experiment(self):
        response = client.post('tasks',
                               data=json.dumps(self.valid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_experiment(self):
        response = client.post('tasks',
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateRetrieveTaskTest(TestCase):
    def setUp(self):
        self.task_1 = Task.objects.create(name="Task 51231223231",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")
        self.task_2 = Task.objects.create(name="Task 512312223",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")

        self.valid_payload = {"name": "Task 5123122323",
                              "priority": "LOW",
                              "end_date": "2020-01-01",
                              "status": "DONE"
                              }
        self.invalid_payload = {"name": "",
                                "priority": "LOW",
                                "end_date": "",
                                "status": "DONE"
                                }

    def test_valid_update_experiment(self):
        response = client.put('tasks', kwargs={'pk': self.task_1.pk},
                              data=json.dumps(self.valid_payload),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_experiment(self):
        response = client.put('tasks', kwargs={'pk': self.task_2.pk},
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteRetrieveTaskTest(TestCase):
    def setUp(self):
        self.task_1 = Task.objects.create(name="Task 512312423231",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")
        self.task_2 = Task.objects.create(name="Task 5123122223",
                                          priority="LOW",
                                          end_date="2020-01-01",
                                          status="DONE")

    def test_valid_delete_experiment(self):
        response = client.delete(
            'tasks', kwargs={'pk': self.task_2.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            'tasks', kwargs={'pk': self.task_2.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
