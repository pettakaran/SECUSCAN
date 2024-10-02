from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key in production

# Configuration for MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/Thaathoi_Boiz"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

# Route for Patient Login
@app.route('/login/patient', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')  # This should correspond to `people_id`
        username = request.form.get('username_patient')
        password = request.form.get('password_patient')

        # Logic to verify patient credentials
        user = mongo.db.Users.find_one({'people_id': patient_id, 'username': username})

        # Debugging: Print the found user
        print("Found User:", user)

        # Verify password if user is found
        if user and user['password'] == password:  # Check without hashing
            flash("Patient login successful!")
            return redirect(url_for('patient_verify'))
        else:
            flash("Invalid Patient ID or Password!")  # Flash error message
            return render_template('index.html')  # Stay on the login page with error message

    return render_template('index')

# Route for Staff Login
@app.route('/login/staff', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        username = request.form.get('username_staff')
        password = request.form.get('password_staff')

        user = mongo.db.Users.find_one({'people_id': staff_id, 'username': username})

        # Debugging: Print the found user
        print("Found User:", user)

        if user and user['password'] == password:  # Check without hashing
            flash("Staff login successful!")
            return redirect(url_for('staff_verify'))
        else:
            flash("Invalid Staff ID or Password!")  # Flash error message
            return render_template('index.html')  # Stay on the login page with error message

    return render_template('index')

# Route for Admin Login
@app.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        username = request.form.get('username_admin')
        password = request.form.get('password_admin')

        user = mongo.db.Users.find_one({'people_id': admin_id, 'username': username})

        # Debugging: Print the found user
        print("Found User:", user)

        if user and user['password'] == password:  # Check without hashing
            flash("Admin login successful!")
            return redirect(url_for('admin_verify'))
        else:
            flash("Invalid Admin ID or Password!")  # Flash error message
            return redirect(url_for('index'))  # Stay on the login page with error message

    return render_template('index')

# Routes for Verification Pages
@app.route('/admin_verify')
def admin_verify():
    return render_template('adminverify.html')

@app.route('/staff_verify')
def staff_verify():
    return render_template('staffverify.html')

@app.route('/patient_verify')
def patient_verify():
    return render_template('patientverify.html')

# Route to register new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password')
        people_id = request.form.get('people_id')

        # Insert the new user into the database
        mongo.db.Users.insert_one({
            'username': username,
            'role': role,
            'password': password,  # Store password as plain text (not recommended for production)
            'people_id': people_id
        })

        flash("User registered successfully!")
        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
