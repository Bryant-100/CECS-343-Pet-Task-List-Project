from check_input import *


class Task:
    def __init__(self, pet_id, task_id, description, status):
        self._pet_id = pet_id
        self._desc = description
        self._status = status
        self._task_id = task_id
    
        
    @property
    def task_id(self):
        return self._task_id
    
    @property
    def desc(self):
        return self._desc
    
    @desc.setter
    def desc(self, new_desc):
        self._desc = new_desc
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status):        
        self._status = new_status
