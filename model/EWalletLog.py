from model.DBSQLAlchemy import db
from sqlalchemy import ForeignKey

class EwalletLog(db.Model):
    __table__name = 'ewallet_log'

    id = db.Column(db.String, primary_key=True)
    status = db.Column(db.Boolean)
    amount = db.Column(db.Integer)
    transaction_type = db.Column(db.String)
    wallet_id = db.Column(db.String, ForeignKey('ewallet.id'))
    reference_id = db.Column(db.String)
    transaction_date = db.Column(db.Date)

