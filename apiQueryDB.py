import pymongo
from sentence_transformers import SentenceTransformer

url = "mongodb+srv://khushboo:1234@onair.bb9ktly.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(url)
db = client["onair"]
collection = db["queries"]
model_name = 'bert-base-nli-mean-tokens'
model = SentenceTransformer(model_name)
    

# return list of all queries in DB
def getQueries():
    query = collection.find()
    data = []
    for i in query:
        data.append([i['query'],i['answer'],i['tags']])
    return data


def insertData(query, title, answer):
    x = collection.insert_one({"title" : title, "query" : query, "tags" : [str(i) for i in model.encode(query.lower())], "answer" : answer})
    return x is not None

