from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import bcrypt
import pyotp
import qrcode
import qrcode.image.svg
import io
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.teardown_appcontext(db.close_connection)

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', username=session.get('username'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Basic validation
        if not username or not password:
            flash('Username and password are required.')
            return render_template('register.html')
            
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        database = db.get_db()
        cursor = database.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_pw.decode('utf-8')))
            database.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except database.IntegrityError:
            flash('Username already exists.')
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        database = db.get_db()
        cursor = database.cursor()
        cursor.execute('SELECT id, username, password_hash, two_factor_enabled FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['temp_user_id'] = user['id']
            session['temp_username'] = user['username']
            if user['two_factor_enabled']:
                return redirect(url_for('verify_2fa'))
            else:
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/setup-2fa')
def setup_2fa():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    database = db.get_db()
    cursor = database.cursor()
    cursor.execute('SELECT two_factor_secret, two_factor_enabled FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    if user['two_factor_enabled']:
        flash('2FA is already enabled.')
        return redirect(url_for('index'))
        
    secret = pyotp.random_base32()
    cursor.execute('UPDATE users SET two_factor_secret = ? WHERE id = ?', (secret, session['user_id']))
    database.commit()
    
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=session['username'], issuer_name='SecureLoginApp')
    
    # Generate SVG QR Code
    img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgPathImage)
    stream = io.BytesIO()
    img.save(stream)
    svg_data = stream.getvalue().decode('utf-8')
    
    return render_template('setup_2fa.html', svg_data=svg_data, secret=secret)

@app.route('/verify-setup-2fa', methods=['POST'])
def verify_setup_2fa():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    token = request.form['token']
    database = db.get_db()
    cursor = database.cursor()
    cursor.execute('SELECT two_factor_secret FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    totp = pyotp.TOTP(user['two_factor_secret'])
    if totp.verify(token):
        cursor.execute('UPDATE users SET two_factor_enabled = 1 WHERE id = ?', (session['user_id'],))
        database.commit()
        flash('2FA successfully enabled!')
        return redirect(url_for('index'))
    else:
        flash('Invalid token. Please try again.')
        return redirect(url_for('setup_2fa'))

@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'temp_user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        token = request.form['token']
        database = db.get_db()
        cursor = database.cursor()
        cursor.execute('SELECT two_factor_secret FROM users WHERE id = ?', (session['temp_user_id'],))
        user = cursor.fetchone()
        
        totp = pyotp.TOTP(user['two_factor_secret'])
        if totp.verify(token):
            session['user_id'] = session['temp_user_id']
            session['username'] = session['temp_username']
            session.pop('temp_user_id', None)
            session.pop('temp_username', None)
            return redirect(url_for('index'))
        else:
            flash('Invalid 2FA token.')
            
    return render_template('verify_2fa.html')

if __name__ == '__main__':
    db.init_db(app)
    app.run(debug=True, port=5000)
