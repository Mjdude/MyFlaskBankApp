from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Transaction Route
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        sender = request.form['sender']
        receiver = request.form['receiver']
        amount = float(request.form['amount'])

        new_transaction = Transaction(sender=sender, receiver=receiver, amount=amount)
        db.session.add(new_transaction)
        db.session.commit()

        return redirect('/transactions')

    all_transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=all_transactions)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)
