import time
from datetime import datetime

from model.DBSQLAlchemy import db
from model.EWallet import EWallet
from model.EWalletLog import EwalletLog
import uuid
from flask import jsonify

class EWalletController:
    def __init__(self, db):
        self.db = db

    def init_ewallet(self, customer_id):
        ewallet = EWallet.query.filter_by(customer_id=customer_id).first()
        token = str(uuid.uuid4()).replace("-", "")

        if ewallet is None:
            newEWallet = EWallet()
            newEWallet.id = str(uuid.uuid4())
            newEWallet.token = token
            newEWallet.customer_id = customer_id
            newEWallet.balance = 0
            newEWallet.status = "disabled"
            self.db.session.add(newEWallet)
            self.db.session.commit()
            return jsonify(
                {
                    "data": {"token": token},
                    "status": "success"
                }
            )
        else:
            ewallet.token = token
            self.db.session.commit()
            return jsonify({
                "data": {"token":token},
                "status":"success"
            })

    def view_ewallet(self, token):
        ewallet = EWallet.query.filter_by(token=token).first()
        if ewallet is None:
            return jsonify(
                {
                    "status":"failed",
                    "data":{
                        "message": f"no ewallet found with token {token}"
                    }
                }
            )
        else:
            if ewallet.status == "disabled":
                return jsonify(
                    {
                        "status": "failed",
                        "data": {
                            "message": f"please enabled ewallet"
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "status":"success",
                        "data": {
                            "wallet": {
                                "id": ewallet.id,
                                "owned_by": ewallet.customer_id,
                                "status": ewallet.status,
                                "enabled_at": ewallet.enable_at,
                                "balance": ewallet.balance
                            }
                        }
                    }
                )

    def deposit_ewallet(self, token, amount, reference_id):
        ewallet = EWallet.query.filter_by(token=token).first()
        ewallet_log = EwalletLog.query.filter_by(reference_id=reference_id).first()

        if ewallet.status == "disabled":
            return jsonify(
                {
                    "status": "failed",
                    "data": {
                        "message": "please enabled ewallet"
                    }
                }
            )

        try:
            amount_parse = int(amount)
        except Exception as ex:
            return jsonify({
                "status": "failed",
                "data": {
                    "message": "Amount must be integer"
                }
            })

        if ewallet_log:
            return jsonify({
                "status":"failed",
                "data": {
                    "message": "Please insert uniqe refences id"
                }
            })
        else:
            date_transaction = datetime.now()
            #reference_id = str(uuid.uuid4())
            ewallet_log = EwalletLog()
            ewallet_log.id = str(uuid.uuid4())
            ewallet_log.amount = amount_parse
            ewallet_log.transaction_type = "deposit"
            ewallet_log.transaction_date = date_transaction
            ewallet_log.wallet_id = ewallet.id
            ewallet_log.reference_id = reference_id
            time.sleep(5)
            ewallet.balance = ewallet.balance + amount_parse
            db.session.add(ewallet_log)
            db.session.commit()
            return jsonify({
                "status": "success",
                "data": {
                    "deposit": {
                        "id": reference_id,
                        "deposited_by": ewallet.id,
                        "status": "success",
                        "deposited_at": date_transaction,
                        "amount": amount_parse,
                        "reference_id": reference_id
                    }
                }
            })


    def withdrawals_ewallet(self, token, amount, reference_id):
        ewallet = EWallet.query.filter_by(token=token).first()
        ewallet_log = EwalletLog.query.filter_by(reference_id=reference_id).first()

        try:
            amount_parse = int(amount)
        except Exception as ex:
            return jsonify({
                "status": "failed",
                "data": {
                    "message": "Amount must be integer"
                }
            })

        if ewallet.balance -amount_parse < 0:
            return jsonify({
                "status": "failed",
                "data": {
                    "message": "Amount withdrawls bigger than balance"
                }
            })

        if ewallet.status == "disabled":
            return jsonify(
                {
                    "status": "failed",
                    "data": {
                        "message": "please enabled ewallet"
                    }
                }
            )


        if ewallet_log is not None:
            return jsonify({
                "status": "failed",
                "data": {
                    "message": "Please insert uniqe refences id"
                }
            })
        else:
            date_transaction = datetime.now()#.strptime("%Y-%m-%d")
            #reference_id = str(uuid.uuid4())
            ewallet_log = EwalletLog()
            ewallet_log.id = str(uuid.uuid4())
            ewallet_log.amount = amount_parse
            ewallet_log.transaction_type = "withdrawals"
            ewallet_log.transaction_date = date_transaction
            ewallet_log.wallet_id = ewallet.id
            ewallet_log.reference_id = reference_id
            time.sleep(5)
            ewallet.balance = ewallet.balance - amount_parse
            db.session.add(ewallet_log)
            db.session.commit()
            return jsonify({
                "status": "success",
                "data": {
                    "deposit": {
                        "id": reference_id,
                        "deposited_by": ewallet.id,
                        "status": "success",
                        "deposited_at": date_transaction,
                        "amount": amount_parse,
                        "reference_id": reference_id
                    }
                }
            })


    def enabled_ewallet(self, token):
        ewallet = EWallet.query.filter_by(token=token).first()
        if ewallet is None:
            return jsonify({
                "status":"Failed",
                "data":{
                    "message":"no ewallet found with this token"
                }
            })
        else:
            if ewallet.status == "enabled":
                return jsonify({
                    "status": "Failed",
                    "data": {
                        "message": "ewallet status must disable to renable again"
                    }
                })

            try:
                ewallet.enable_at = datetime.now()
                ewallet.status = "enabled"
                db.session.commit()
                return jsonify({
                    "status": "Success",
                    "data": {
                        "wallet": {
                            "id": ewallet.id,
                            "owned_by": ewallet.customer_id,
                            "status": ewallet.status,
                            "enabled_at": ewallet.enable_at,
                            "balance": ewallet.balance
                        }
                    }
                })

            except Exception as ex:
                db.session.rollback()
                return jsonify({
                    "status": "Failed",
                    "data": {
                        "message": "Failed update"
                    }
                })



    def disable_ewallet(self, token):
        ewallet = EWallet.query.filter_by(token=token).first()
        if ewallet is None:
            return jsonify({
                "status": "Failed",
                "data": {
                    "message": "no ewallet found with this token"
                }
            })
        else:
            ewallet.disable_at = datetime.now()
            ewallet.status = "disabled"
            db.session.commit()
            return jsonify({
                "status": "Success",
                "data": {
                    "wallet": {
                        "id": ewallet.id,
                        "owned_by": ewallet.customer_id,
                        "status": ewallet.status,
                        "disabled_at": ewallet.disable_at,
                        "balance": ewallet.balance
                    }
                }
            })