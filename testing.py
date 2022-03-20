import time
from locust import HttpUser, TaskSet, task, between

class SubClassTest(TaskSet):

    @task
    def main_page(self):
        body = {
            "nama":"Tas Kipling",
            "kategori": "Tas",
            "deskripsi": "Tas ransel untuk travelling",
            "is_available":True
        }
        self.client.post('/product', json=body)

    @task(2)
    def perihal_page(self):
        self.client.get('/')


class MainClassTest(HttpUser):
    tasks = [SubClassTest]
    wait_time = between(5, 10)