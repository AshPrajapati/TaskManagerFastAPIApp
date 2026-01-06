class EmailService:
    def send_email_on_task_created(self, task):
        print(f"Task created: title:{task.title}")

    def send_email_on_task_completed(self, task):
        print(f"Task completed: title:{task.title}")
