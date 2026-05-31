import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "fallback-low-security-key")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///local_test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password_hash = db.Column(db.String(200), nullable=False)

#--- ROUTES ---

@app.route('/')
def home():
	return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form.get('username').strip()
		password = request.form.get('password')

		if not username or not password:
			flash("Username and password cannot be empty!", "danger")
			return redirect(url_for('register'))

		hashed_password = generate_password_hash(password, method='scrypt')

		new_user = User(username=username, password_hash=hashed_password)
		try:
			db.session.add(new_user)
			db.session.commit()
			flash("Registration successful! Please login.", "success")
			return redirect(url_for('login'))
		except:
			db.session.rollback()
			flash("Username already exists", "danger")

	return'''
		<h2>Register</h2>
		<form method = "post">
			<input type = "text" name = "username" placeholder = "Username" required><br><br>
			<input type = "password" name = "password" placeholder = "Password" required><br><br>
			<button type = "submit"> Register </button>
		</form>
		<p>Already have an account? <a href="/login">Login here</a></p>
'''


@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		user = User.query.filter_by(username=username).first()

		if user and check_password_hash(user.password_hash, password):
			session['user_id'] = user.id
			session['username'] = user.username
			return redirect(url_for('dashboard'))
		else:
			flash("Invalid username or password.", "danger")
	return '''
			<h2>Login</h2>
			<form method="post">
				<input type="text" name="username" placeholder="Username" required><br><br>
				<input type = "password" name="password" placeholder="Password" required><br><br>
				<button type ="submit">Login</button>
			</form>
			<p>Don't have an account? <a href="/register">Register here</a></p>
			'''

@app.route('/dashboard')
def dashboard():
	if 'user_id' not in session:
		flash("Please log in to access this page.", "warning")
		return redirect(url_for('login'))
	return f'''
		<h2>Dashboard</h2>
		<p>Welcome, {session['username']}! You are securely logged in.</p>
		<a href="/logout"><button>Logout</button></a>
'''

@app.route('/logout')
def logout():
	session.clear()
	flash("You have been logged out.", "info")
	return redirect(url_for('login'))


with app.app_context():
	db.create_all()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 5000)
