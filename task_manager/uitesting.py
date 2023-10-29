from flask.test import TestCase
from flask.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

option = webdriver.EdgeOptions()
driver = webdriver.Edge(options=option)
driver.get("http://156.0.0.1:8000/task/")  

add = driver.find_element(By.LINK_TEXT, "Add Task")  

title = driver.find_element(By.NAME, "title")  
title.send_keys("Book order")
description = driver.find_element(By.NAME, "description") 
description.send_keys("New Harry Potter book")
date = driver.find_element(By.NAME, "date")  
date.send_keys("15.11.2023")
print(title)
print(description)
print(date)
time.sleep(3)
modify = driver.find_element(By.NAME, "button")  
modify.click()

time.sleep(3)

class TaskCRUDTests(LiveServerTestCase): 
 def test_delete_task(self):
        
        driver.get("http://156.0.0.1:8000/task/12/delete")  
        self.assertIn("Delete Record", driver.title)

        # Check if the "Delete" button is present
        delete_button = driver.find_element(By.XPATH, '//button[contains(@name, "Delete")][contains(@value, "Delete")][contains(@class, "btn btn-warning")]')  
        self.assertIsNotNone(delete_button)

        # Perform the delete action
        delete_button.click()

        # Wait for a brief moment to let the delete action complete (adjust the wait time if necessary)
        time.sleep(3)

        # Check if the task has been deleted 
        driver.get(self.live_server_url + '/task/')  # Navigate to the task list page  
        task_titles = driver.find_elements(By.XPATH, '//td[contains(@class, "title")]') 
        task_titles = [title.text for title in task_titles]  
        self.assertNotIn("Book order", task_titles)

    def test_update_task(self):  
        driver.get("http://156.0.0.1:8000/task/") 
        self.assertIn("Assignment of Tasks", driver.title)  

        # Check if there are tasks listed  
        tasks = driver.find_elements(By.TAG_NAME, 'tr')  

        # Assuming you have at least one task to update  
        if len(tasks) > 1:
            # Click the "Edit" button of the first task in the table 
            edit_button = tasks[1].find_element(By.PARTIAL_LINK_TEXT, "Edit")  
            edit_button.click()

            # Check if we are on the update page

            # Find the form input fields by name and update the task information  
            title_input = driver.find_element(By.NAME, "title") 
            title_input.clear()
            title_input.send_keys("Updated")

            date_input = driver.find_element(By.NAME, "date")  
            date_input.clear()
            date_input.send_keys("Updated")

            description_input = driver.find_element(By.NAME, "description")  
            description_input.clear()
            description_input.send_keys("35")

            # Submit the form
            submit_button = driver.find_element(By.NAME, "button") 
            submit_button.click()

            # Check if we are redirected back to the task list page 
            self.assertIn("Assignment of Tasks", driver.title)  

            # Check if the task's information has been updated 
            updated_task = driver.find_element(By.XPATH, f'//td[text()="Updated"]') 
            self.assertIsNotNone(updated_task)
        else:
            self.skipTest("No tasks available for update")  
driver.quit
