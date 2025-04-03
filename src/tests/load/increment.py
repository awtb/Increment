from locust import HttpUser, task


class IncrementUser(HttpUser):
    @task
    def increment(self):
        self.client.post("/api/v1/increment")
