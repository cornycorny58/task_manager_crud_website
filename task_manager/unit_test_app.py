import unittest
from flask import Flask
from pymongo import MongoClient
from classes import CreateTask, DeleteTask, UpdateTask, ResetTask
from app import createTask, deleteTask, updateTask, resetTask, updateTaskID

class TestApp(unittest.TestCase):
    def setUp(self):
        #In Python, self is a conventionally used name for the first parameter of methods in a class.
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'mysecretkey'
        self.client = self.app.test_client()
      #The setUp method initializes a Flask test client and creates a test context.

    def test_createTask(self):
        with self.app.app_context():
            form = CreateTask(title='Test Title', priority='High', shortdesc='Test Description')
            response = createTask(form)
            self.assertEqual(response.status_code, 302)  # Check if it redirects
          # Each test method creates the necessary form instances, calls the corresponding function, and asserts that the response is a redirect (status code 302)

    def test_deleteTask(self):
        with self.app.app_context():
            form = DeleteTask(key=1, title='Test Title')
            response = deleteTask(form)
            self.assertEqual(response.status_code, 302)  # Check if it redirects

    def test_updateTask(self):
        with self.app.app_context():
            form = UpdateTask(key=1, shortdesc='Updated Description')
            response = updateTask(form)
            self.assertEqual(response.status_code, 302)  # Check if it redirects

    def test_resetTask(self):
        with self.app.app_context():
            response = resetTask(ResetTask())
            self.assertEqual(response.status_code, 302)  # Check if it redirects

    def test_updateTaskID(self):
       #The test_updateTaskID method tests the updateTaskID function separately.
        with self.app.app_context():
            initial_value = MongoClient('localhost:27017').db.settings.find_one({'name': 'task_id'})['value']
            updateTaskID(1)
            updated_value = MongoClient('localhost:27017').db.settings.find_one({'name': 'task_id'})['value']
            self.assertEqual(updated_value, initial_value + 1)

if __name__ == '__main__':
    unittest.main()
