# ----------------------------
# GAMESHARE Sale API
# Component Lead: Syed Safwaan
# ----------------------------

import datetime as dt
import json
from flask import Flask, request
from flask_cors import CORS
from firebase_admin import initialize_app, credentials, firestore

# Connect to Firestore db services
certs = credentials.Certificate('serviceAccountKey.json')
initialize_app(certs)
db = firestore.client()

# Set up Flask
app = Flask(__name__)
CORS(app)

required_fields = "game", "user", "soldFor"
optional_fields = ()


# ----- API FUNCTIONALITY
@app.route('/sales', methods=['GET'])
def get_all_sales():
    """ Returns all sales in the Firestore 'sales' collection. """
    data = db.collection('sales').get()
    sales = [doc.to_dict() for doc in data]
    return json.dumps(sales, indent=4, sort_keys=True, default=str)


@app.route('/sales/sale/<sid>', methods=['GET'])
def get_sale(sid):
    """ Returns sale referenced by 'sid' in Firestore collection. """
    [data] = db.collection('sales').where('sid', '==', sid).get()
    sale = data.to_dict()
    return sale


@app.route('/sales/user/<uid>', methods=['GET'])
def get_sale(uid):
    """ Returns sales referenced by 'uid' in Firestore collection. """
    data = db.collection('sales').where('uid', '==', uid).get()
    sales = [doc.to_dict() for doc in data]
    return json.dumps(sales, indent=4, sort_keys=True, default=str)


@app.route('/sales/create/', methods=['POST'])
def create_sale():
    """ Creates sale with POST request data within Firestore collection. """
    form = request.form

    time = dt.datetime.now()
    sale_data = {
        field: form[field] for field in required_fields
    } | {
        field: form.get(field, None) for field in optional_fields
    }

    _, doc = db.collection('sales').add(sale_data)  # initial data
    db.collection('sales').document(doc.id).update({  # document-related data
        "sid": doc.id,
        "createDate": time,
    })

    return "Sale successfully created", 201


@app.route('/sales/delete', methods=['DELETE'])
def delete_sale():
    """ Deletes sale referenced by 'sid' within Firestore collection. """
    form = request.form
    sid = form["sid"]

    db.collection('sales').document(sid).delete()
    return "Sale successfully deleted", 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4005, debug=True)
