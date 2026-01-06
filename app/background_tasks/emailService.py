class EmailService:
    def send_email_on_task_created(self, task):
        print(f"Task created: title:{task.title}")
