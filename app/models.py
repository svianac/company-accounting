from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FinancialEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<FinancialEntry {self.id} - Amount: {self.amount} on {self.date}>'