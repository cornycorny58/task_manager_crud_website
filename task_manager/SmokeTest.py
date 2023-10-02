import unittest
from flask import Flask
from flask_testing import TestCase
from flask import Flask, render_template, redirect
from pymongo import MongoClient
from classes import *

class SmokeTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        return app

    def setUp(self):
        # Initialize the Flask app and test client
        self.app = self.create_app()
        self.client = self.app.test_client()

        # Create a test database and configure the application to use it
        self.app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_TaskManager'
        self.app.config['SECRET_KEY'] = 'mysecretkey'

        # Initialize the database and perform any setup tasks
        with self.app.app_context():
            self.client = MongoClient('localhost:27017')
            db = self.client.test_TaskManager

            # Insert test data or perform any necessary setup
            if db.settings.find({'name': 'task_id'}).count() <= 0:
                db.settings.insert_one({'name': 'task_id', 'value': 0})

    def tearDown(self):
        # Clean up any resources or databases used in the tests
        self.client.drop_database('test_TaskManager')

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Title', response.data)  # Check if the form is present

    def test_create_task(self):
        response = self.client.post('/', data={
            'cform-title': 'Test Task',
            'cform-priority': '1',
            'cform-shortdesc': 'Test Description',
            'cform-create': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)  # Check if the newly created task is displayed

    def test_delete_task(self):
        # Create a test task first
        self.client.post('/', data={
            'cform-title': 'Test Task',
            'cform-priority': '1',
            'cform-shortdesc': 'Test Description',
            'cform-create': True
        }, follow_redirects=True)

        response = self.client.post('/', data={
            'dform-title': 'Test Task',
            'dform-delete': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Task', response.data)  # Check if the task is deleted

if __name__ == '__main__':
    unittest.main()
