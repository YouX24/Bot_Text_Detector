from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Root = endpoint to get data
@app.route("/detection", methods=["POST"])
def text_detection():
    data = request.get_json()
    
    # TODO input data text into ml, return output result as response back to frontend
    
    return jsonify(data["text"])


if __name__ == "__main__":
    app.run(debug=True)





# @app.route("/get-user/<user_id>") # path parameter = dynamic value that can be passed in the path URL, that can be accessed inside of our route
# def get_user(user_id):
#     user_data = {
#         "user_id": user_id,
#         "name": "John Doe",
#         "email": "johndoe@example.com",
#     }
    
#     # query parameter = extra value included after main path, exmaple: /get-user/<id>?extra="value"
#     extra = request.args.get("extra")
#     if extra:
#         user_data["extra"] = extra
        
#     return jsonify(user_data), 200


# need to specific HTTP Method if method is not GET
# @app.route("/create-user", methods=["POST", "GET"])
# def create_user():
#     if request.method == "POST":
#         data = request.get_json() # get all json in body of request
#         return jsonify(data), 201