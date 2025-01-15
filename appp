from flask import Flask, session, render_template, request, redirect, url_for
from auth import check_login_validity, get_user_id, check_name_availability, create_user
from src.api import get_all_available_coins
from db import get_all_asset_data, insert_into_assets
from src.dashboard import generate_dashboard, check_valid_date, get_number_of_coins

app = Flask(__name__)
app.secret_key = 'secret_key'

def get_user_assets(user_id):
    return [
        {
            'id': asset[0],
            'user_id': asset[1],
            'coin': asset[2],
            'amount': asset[3],
            'date': asset[4]
        }
        for asset in get_all_asset_data() if asset[1] == user_id
    ]

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user_id = session.get('id')
    if not user_id:
        return redirect(url_for('login'))

    user_assets = get_user_assets(user_id)
    if not user_assets:
        return render_template('init.html')

    config = generate_dashboard(user_assets, 'usd')
    if config in ['connection error', 'rate limit reached']:
        return render_template(f'{config.replace(" ", "_")}.html')

    return render_template('dashboard.html', config=config)

@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    user_id = session.get('id')
    if not user_id:
        return redirect(url_for('login'))

    user_assets = get_user_assets(user_id)
    if get_number_of_coins(user_assets) >= 40:
        return redirect(url_for('dashboard'))

    supported_coins = get_all_available_coins()
    if request.method == 'POST':
        coin, amount, date = request.form.get('coin'), request.form.get('amount'), request.form.get('date')
        messages = {
            'coin': '' if coin in supported_coins else 'The coin you entered is not supported.',
            'amount': '',
            'date': '' if check_valid_date(date) else 'Invalid date format. Use: dd-mm-yyyy.'
        }

        if any(messages.values()):
            return render_template('add_asset.html', coins=supported_coins, messages=messages)

        insert_into_assets(user_id, coin, float(amount), date)
        return redirect(url_for('dashboard'))

    if supported_coins in ['connection error', 'rate limit reached']:
        return render_template(f'{supported_coins.replace(" ", "_")}.html')

    return render_template('add_asset.html', coins=supported_coins, messages={'coin': '', 'amount': '', 'date': ''})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        if check_login_validity(username, password):
            session['id'] = get_user_id(username)
            return redirect(url_for('index'))

        return render_template('login.html', username_message='Invalid username.', password_message='Invalid password.')

    return render_template('login.html', username_message='', password_message='')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        if check_name_availability(username):
            create_user(username, password)
            return redirect(url_for('login'))

        return render_template('register.html', username_message='Username unavailable.', password_message='')

    return render_template('register.html', username_message='', password_message='')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
