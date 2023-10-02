import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from pymongo import MongoClient
from classes import *

class IntegrationTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'mysecretkey'
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/TaskManagerTest'  # Use a separate test database
        return app

    def setUp(self):
        self.client = self.app.test_client()

    def tearDown(self):
        mongo_client = MongoClient('localhost', 27017)
        mongo_client.drop_database('TaskManagerTest')

    def test_create_update_delete_task(self):
        # Create a task
        response = self.client.post('/create', data={
            'title': 'Integration Test Task',
            'priority': 1,
            'shortdesc': 'Test Description'
        })
        self.assertRedirects(response, '/')

        # Update the task
        response = self.client.post('/update', data={
            'key': 1,
            'shortdesc': 'Updated Test Description'
        })
        self.assertRedirects(response, '/')

        # Verify that the task was updated
        response = self.client.get('/')
        self.assert200(response)
        self.assertIn(b'Updated Test Description', response.data)

        # Delete the task
        response = self.client.post('/delete', data={'key': 1})
        self.assertRedirects(response, '/')

        # Verify that the task was deleted
        response = self.client.get('/')
        self.assert200(response)
        self.assertNotIn(b'Updated Test Description', response.data)

if __name__ == '__main__':
    unittest.main()
