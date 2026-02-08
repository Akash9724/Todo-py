from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
import pymongo



load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')



client = pymongo.MongoClient(MONGO_URI)
db = client.todo_db
collection = db['todo_items']



app = Flask(__name__)



@app.route('/')
def Home():
    return render_template('todo.html')



@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    try:
        form_data = dict(request.form)

        # optional validation
        if not form_data.get("itemName") or not form_data.get("itemDescription"):
            return "Missing fields"

        collection.insert_one(form_data)

        return "Todo item submitted successfully"

    except Exception as e:
        return render_template('todo.html', error=str(e))



@app.route('/api/todos')
def view():
    data = collection.find()
    data = list(data)

    for item in data:
        del item['_id']

    return {
        "data": data
    }


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
