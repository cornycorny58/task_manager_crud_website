from locust import HttpUser, task, between

class TaskManagerUser(HttpUser):
    wait_time = between(2, 5)

    @task(1)
    def view_homepage(self):
        self.client.get("/")
      #
    @task(2)
    def create_task(self):
        self.client.get("/add_task/")  

    @task(3)
    def delete_task(self):
        self.client.get("/delete_task/") 

    @task(4)
    def update_task(self):
        self.client.get("/update_task/")  

    @task(5)
    def reset_task(self):
        self.client.get("/reset_task/")  

