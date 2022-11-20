from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Task:
    db = "tudu"
    def __init__(self, data):
        self.id = data['id']
        self.task_name = data['task_name']
        self.priority = data['priority']
        self.category = data['category']
        self.due_date = data['due_date']
        self.notes = data['notes']


    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM tudu.task LEFT JOIN user on task.user_id = user.id WHERE user.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO tudu.task (task_name , priority , category , due_date, notes, user_id) VALUES ( %(task_name)s , %(priority)s , %(category)s , %(due_date)s , %(notes)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM tudu.task WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results[0]

    @classmethod
    def update(cls,data):
        print(data)
        query = "UPDATE tudu.task SET task_name=%(task_name)s, priority=%(priority)s, category=%(category)s, due_date=%(due_date)s, notes=%(notes)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM task WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def is_valid_task(task):
        is_valid = True

        if len(task["task_name"]) <= 0:
            is_valid = False
            flash("Task name is required.")
        if len(task["task_name"]) <= 2:
            is_valid = False
            flash("Task name must be at least 3 characters.")
        if len(task["priority"]) <= 0:
            is_valid = False
            flash("Priority is required.")
        if len(task["category"]) <= 0:
            is_valid = False
            flash("Category is required")
        if len(task["due_date"]) <= 0:
            is_valid = False
            flash("Due date is required.")
        return is_valid


    @classmethod
    def get_all_user_tasks(cls, data ):
        query = "SELECT * FROM tudu.task LEFT JOIN user on task.user_id = user.id WHERE task.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        user = cls(results[0])
        for row in results:
            s = {
                'id': row['id'],
                'user_id': row['user_id.id'],
                'task_name': row['task_name'],
                'priority': row['priority'],
                'category': row['category'],
                'due_date': row['due_date'],
            }
            user.tasks.append( Task(s) )
        return user