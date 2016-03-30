# -*- coding=utf-8 -*-
import json
from sjgtw.tree.tree import Node
import os


def json2tree(json):
    pass


path = os.getcwd()
json = json.load(open("../sjgtw_catalog.json", "r"))
# 读取所有jsonobj,将<id, node>放入dict
dictAll = {}

for jsonObj in json:
    node = Node(jsonObj)
    dictAll[jsonObj['clickId']] = node

# 遍历dict, 为每个node找到parent
for clickId, node in dictAll.items():
    if 'parentClickId' in node.data:
        dictAll[node.data['parentClickId']].add_child(node)

dictAll[0].walkAndFindLeaves()

# print(path)
