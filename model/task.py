class Task:
    def __init__(self, task_json):
        self.title = task_json['title']
        self.description = task_json['description']
