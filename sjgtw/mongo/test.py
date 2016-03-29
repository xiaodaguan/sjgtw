import pymongo
import json

connection = pymongo.MongoClient("mongodb://guanxiaoda.cn:27017")
db = connection['sjgtwdb']

collection = db['sjgtw_info']

pipeline = [
    {
        "$group":{
            "_id":"$url","count":{"$sum":1}
        }
    }

]

result = list(collection.aggregate(pipeline))
json.dump(result,open("sjgtw_crawledinfo.json","w"))
print(len(result))
