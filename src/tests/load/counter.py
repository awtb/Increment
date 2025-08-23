from locust import HttpUser, task


class CounterUser(HttpUser):
    @task
    def increment(self):
        self.client.post("/api/v1/counter")
