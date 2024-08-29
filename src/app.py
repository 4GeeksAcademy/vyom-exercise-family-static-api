"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)



# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# jackson_family.add_member({
#     'first_name': 'John',
#     'age': 33,
#     'lucky_numbers': [7, 13, 22]
# })

# jackson_family.add_member({
#     'first_name': 'Jane',
#     'age': 35,
#     'lucky_numbers': [10, 14, 3]
# })

# jackson_family.add_member({
#     'first_name': 'Jimmy',
#     'age': 5,
#     'lucky_numbers': [1]
# })

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    # if request.content_type != 'application/json':
    #     return jsonify({'error': 'content-type tiene que ser application/json'}), 400
    
    try:
        members = jackson_family.get_all_members()

        if members == []:
            return jsonify({'error': 'No hay miembros', 'code_status': 404}), 404
        

        
        return jsonify(members), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    # if request.content_type != 'application/json':
    #     return jsonify({'error': 'content-type tiene que ser application/json'}), 400
    
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({'error': 'Miembro no encontrado'}), 404
        return jsonify(member), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/member', methods=['POST'])
def add_member():
    if request.content_type != 'application/json':
        return jsonify({'error': 'content-type tiene que ser application/json'}), 400

    try:
        member = request.get_json()
        mandatorys = ['first_name', 'age', 'lucky_numbers']
        for require in mandatorys:
            if require not in member:
                return jsonify({'error': f'Falta este dato: {require}'}), 400
        
        if not isinstance(member['age'], int) or member['age'] <= 0:
            return jsonify({'error': 'Edad tiene que ser mayor a 0'}), 400
            

        jackson_family.add_member(member)
        return jsonify(member), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    # if request.content_type != 'application/json':
    #     return jsonify({'error': 'content-type tiene que ser application/json'}), 400
    
    try:
        jackson_family.delete_member(member_id)
        return jsonify({'done': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/members', methods=['GET'])
# def handle_hello():

#     # this is how you can use the Family datastructure by calling its methods
#     members = jackson_family.get_all_members()
#     response_body = {
#         "hello": "world",
#         "family": members
#     }


#     return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
