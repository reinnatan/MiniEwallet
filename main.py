from controller.EWalletController import EWalletController
from flask import Flask, jsonify, request

from middleware.Middleware import token_required
from model.DBSQLAlchemy import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ewallet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BASE_END_POINT = "/api/v1"
db.init_app(app)
wallController = EWalletController(db)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route(BASE_END_POINT+"/init", methods=['POST'])
def init_ewallet():
    customer_id = request.form['customer_xid']
    response = wallController.init_ewallet(customer_id)
    return response


@app.route(BASE_END_POINT+"/wallet", methods=['GET', 'POST', 'PATCH'])
@token_required
def view_ewallet(ewallet):
    if request.method == "GET":
        return wallController.view_ewallet(ewallet.token)
    elif request.method == "POST":
        return wallController.enabled_ewallet(ewallet.token)
    elif request.method ==  "PATCH":
        return wallController.disable_ewallet(ewallet.token)
    else:
        return jsonify({"success":"Failed", "message":"Method not allow this endpoint"})

@app.route(BASE_END_POINT+"/wallet/deposits", methods=['POST'])
@token_required
def deposits_ewallet(ewallet):
    amount = request.form['amount']
    reference_id = request.form['reference_id']
    return wallController.deposit_ewallet(ewallet.token, amount, reference_id)

@app.route(BASE_END_POINT+"/wallet/withdrawals", methods=['POST'])
@token_required
def withdraw_ewallet(ewallet):
    amount = request.form['amount']
    reference_id = request.form['reference_id']
    return wallController.withdrawals_ewallet(ewallet.token, amount, reference_id)

@app.before_first_request
def create_table():
    db.create_all()

if __name__ == '__main__':
    app.run()