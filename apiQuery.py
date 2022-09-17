from flask import Flask, request
import simplejson
from apiQueryDB import getQueries, insertData
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



app = Flask("__main__")

@app.route('/')
def hi():
  return "Hello"

@app.route('/queryCheck', methods = ["POST"])
def checkQuery():
    isans = False
    ret = ""
    model_name = 'bert-base-nli-mean-tokens'

    query = request.get_json()['query']

    model = SentenceTransformer(model_name)
    dataDB = getQueries()
    sentence_vecs = [i[2] for i in dataDB]

    ans = cosine_similarity(
        model.encode([query]),
        sentence_vecs
    )


    maxSim = max(ans[0])

    if(maxSim > 0.7):
        maxIndex = list(ans[0]).index(maxSim)
        ret = dataDB[maxIndex][1]
        isans = True
    
    return simplejson.dumps({"ans" : f"{ret}", "isans" : isans}, ignore_nan = True)

    

@app.route('/add', methods = ["POST"])
def newQ():
    query = request.get_json()['query'].lower()
    title = request.get_json()['title'].lower()
    answer = request.get_json()['answer'].lower()
    return simplejson.dumps({"status" : insertData(query, title,answer)}, ignore_nan = True)


if __name__ == "__main__":
  app.run(debug = True)
