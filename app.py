from classes.admin import Admin
from classes.user import User
from classes.forms import LoginForm, RegistrationForm
from flask import Flask, render_template, flash, redirect, url_for, session, request
import tokens
import json
import databases_init
import hashlib
from data.person_number_checker import personnummer_checker, gender_checker


app = Flask(__name__)

#protect from CSRF attacks
app.config['SECRET_KEY'] = tokens.generate_token()

translations = "lang.json"
company_name = "Discovers Company"

def read_file_json(filename):
    try:
        with open(filename, encoding = "utf-8") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {}


def hash_password(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


@app.route('/')
def index():
    main_page = True
    #current Dummy data
    visitor = 1
    return render_template('index.html', visitor = visitor, company_name= company_name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if personnummer_checker(form.person_number.data):
            databases_init.insert_customer(form.person_number.data ,form.first_name.data, form.last_name.data, form.email.data, hash_password(form.password.data), form.phone.data, form.address.data)
            flash(f"Account created for {form.first_name.data} {form.last_name.data}!", "success")
            return redirect(url_for('login'))
        flash("Wrong personal number!", "danger")
        return redirect(url_for('register'))
    else:
        flash("Registration failed. Please try again.", "danger")

    return render_template('register.html', title='Register' , form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_pass = hash_password(password)
        check = databases_init.check_customer(email, hashed_pass)

        if check is not None:
            session["id"] = check[0]
            print(f"Successfully logged in {check[2]} {check[3]}")
            flash(f"Successfully logged in! Welcome {check[2]} {check[3]}", "success")
            return redirect(url_for('home'))
        else:
            flash("Login failed. Please try again.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if "id" in session:
        user_id = session["id"]
        current_info = databases_init.get_information_from_id(user_id)
        if len(current_info) != 0:
            first_name = current_info[2]
            return render_template("home.html", title="Home",user_id = user_id, first_name=first_name)
        return redirect(url_for('login'))
    else:
        return redirect(url_for("login"))


@app.route('/about')
def about():
    # get lang from URL query string (?lang=swedish) default to english
    lang = request.args.get("lang", "english")
    return render_template('about.html', title='About', lang=lang, translation=read_file_json(translations))

@app.route('/developer')
def developer():
    return render_template('developer.html', title='Developer')

@app.route('/logout')
def logout():
    session.pop("id", None)
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    '''
    user_a = User("Najem Aldeen", "Abu Hamdah", "ngmaldin7@gmail.com", "test", "1998", "2", "14")
    user_b = Admin("Najem2 Aldeen", "Abu Hamdah", "ngmaldin7@gmail.com", "test", "1998", "2", "14")

    print(user_a.__str__())
    print()
    print(user_b.__str__())
    '''
    app.run(debug=True)

