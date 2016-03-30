
import json


class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def walk(self):
        print(str(self.data))
        if self.children:
            for child in self.children:
                child.walk()

    def walkAndFindLeaves(self):

        # print(str(self.data))
        if self.children:
            for child in self.children:
                child.walkAndFindLeaves()
        else:
            print(json.dumps(self.data,ensure_ascii= False)+",")