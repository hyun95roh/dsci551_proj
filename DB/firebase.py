import pandas as pd
import json
import requests

class myfireDB: 
    def __init__(self):
        # Database connection parameters
        self.testbase_url ="https://dsci551-2f357-default-rtdb.firebaseio.com/"
        self.connection = None
        self.response = None 
        self.request_url = None 

    def status_check(self): 
        # Check for errors
        if self.response.status_code != 200:
            print(f"Failed to work on the node: {self.response.status_code}, {self.response.text}")
        else:
            print(f"Successfully done: {self.response.text}") 

    def search(self, node:str, filter):
        self.get(node, filter)

    def get(self, node=None, filter=None):
        if filter is None:
            self.request_url = f"{self.testbase_url}/{node}.json"
        else :
            self.request_url = f"{self.testbase_url}/{node}.json?{filter}"            
        self.response = requests.get(self.request_url)
        #self.status_check()
        return self.response.content 

    def delete(self, node): 
        # DELETE the specific node 
        self.request_url = f"{self.testbase_url}/{node}.json"
        # Send a DELETE request to remove all nodes under /sales
        self.response = requests.delete(self.request_url)
        self.status_check()

    
    def put(self, node, data:dict):
        self.request_url = f"{self.testbase_url}/{node}.json"
        self.response = requests.put(self.request_url, json=data)
        self.status_check()

    def post(self, node, data:dict): 
        self.request_url = f"{self.testbase_url}/{node}.json"
        self.response = requests.post(request_url, json=data)
        self.status_check()



