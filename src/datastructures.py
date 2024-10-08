
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        # example list of members
        self._members = [
            {"id": 1, "name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
            {"id": 2, "name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
            {"id": 3, "name": "Jimmy", "age": 5, "lucky_numbers": [1]}
        ]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        generateId = self._next_id
        self._next_id += 1
        return generateId


    def add_member(self, member):
        # fill this method and update the return
        if 'id' not in member:
            member['id'] = self._generateId()
        member['last_name'] = self.last_name
        self._members.append(member)

    def delete_member(self, id):
        # fill this method and update the return
        new_members = []
        for member in self._members:
            if member['id']  != id:
                new_members.append(member)
        self._members = new_members

    def get_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member['id'] == id:
                return member
        return None
        
    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
