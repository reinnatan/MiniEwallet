from model.DBSQLAlchemy import db

class EWallet(db.Model):
    __tablename__ = "ewallet"
    id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String)
    enable_at = db.Column(db.Date)
    disable_at = db.Column(db.Date)
    balance = db.Column(db.Integer)
    customer_id = db.Column(db.String)
    token = db.Column(db.String)

