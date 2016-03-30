# -*- coding=utf-8 -*-
import json
from sjgtw.tree.tree import Node
import os


def json2tree(json):
    pass


path = os.getcwd()
cata = json.load(open("../sjgtw_catalog.json", "r"))
# 读取所有jsonobj,将<id, node>放入dict
jsonStr = '  {\"clickId\": 3,    \"name\": \"生铁、铁合金\"}'
root = Node(json.loads(jsonStr))

dictAll = {}

for jsonObj in cata:
    node = Node(jsonObj)
    dictAll[jsonObj['clickId']] = node

# 遍历dict, 为每个node找到parent
for clickId, node in dictAll.items():
    if 'parentClickId' in node.data:
        dictAll[node.data['parentClickId']].add_child(node)
    else:
        root.add_child(node)


root.walkAndFindLeaves()

# print(path)
