#from classes.admin import Admin
#from classes.user import User
import flask

from classes.forms import LoginForm, RegistrationForm
from flask import Flask, render_template, flash, redirect, url_for, session, request
import tokens, json, hashlib, databases_init, calendar
from data.checker import check_if_admin
from data.person_number_checker import personnummer_checker, gender_checker
from classes.forms import ReservationForm
from datetime import date, timedelta


app = Flask(__name__)

#protect from CSRF attacks
app.config['SECRET_KEY'] = tokens.generate_token()
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(days=365)

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

@app.after_request
def add_cache_headers(resp):
    if request.path.startswith('/static/videos/'):
        resp.cache_control.public = True
        resp.cache_control.max_age = 31536000
    return resp


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
            state = databases_init.insert_customer(
                form.person_number.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                hash_password(form.password.data),
                form.phone.data,
                form.address.data,
            )
            if state:
                flash(f"Account created for {form.first_name.data} {form.last_name.data}!", "success")
                return redirect(url_for('login'))
            flash(f"user already exist!", "danger")
            return redirect(url_for('register'))
        flash("Wrong personal number!", "danger")
    if request.method == 'POST' and not form.validate():
        flash("Please fix the errors below.", "danger")
    return render_template('register.html', title='Register', form=form)

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
            current_permission = check_if_admin(check)
            if current_permission:
                session['admin'] = True
                flash(f"Admin successfully logged in! Welcome {check[2]} {check[3]}", "success")
                return redirect(url_for('admin_db'))
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
        if current_info:
            first_name = current_info[2]  # assuming index 2 is first_name
            last_name = current_info[3]
            return render_template("home.html", title="Home", user_id=user_id, first_name=first_name, last_name=last_name)
    return redirect(url_for('login'))


@app.route("/reserve", methods=["GET", "POST"])
def reserve():
    if "id" not in session:
        return redirect(url_for("login"))

    user_id = session["id"]
    cu = databases_init.get_information_from_id(user_id)
    form = ReservationForm()
    today_iso = date.today().isoformat()
    form.day.render_kw = {"min": today_iso}

    selected_day = (form.day.data or date.today())
    booked = databases_init.get_booked_slots(selected_day.isoformat())
    form.slot.choices = [(s, s) for s in databases_init.SLOTS if s not in booked] or [(s, s) for s in databases_init.SLOTS]

    if form.validate_on_submit():
        day_iso = form.day.data.isoformat()
        full_name = f"{cu[2]} {cu[3]}"; email = cu[4]
        ok = databases_init.insert_reservation(day_iso, form.slot.data, full_name.strip(), email.strip())
        if ok:
            flash(f"Booked {form.slot.data} on {day_iso} for {full_name}.", "success")
            return redirect(url_for("reserve"))
        flash("That slot is already booked. Please choose another.", "warning")
        return redirect(url_for("reserve"))

    return render_template("reserve.html", form=form, first_name=cu[2], last_name=cu[3], email=cu[4])


@app.route("/admin_db", methods=["GET", "POST"])
def admin_db():
    if "id" not in session or not session.get("admin"):
        return redirect(url_for("login"))

    user_id = session["id"]
    current_info = databases_init.get_information_from_id(user_id)
    if not current_info:
        session.clear()
        return redirect(url_for("login"))

    first_name = current_info[2]
    last_name = current_info[3]

    form = RegistrationForm()
    all_users = {}

    if request.method == "POST":
        if form.validate_on_submit():
            # validate Swedish personal number, etc.
            if personnummer_checker(form.person_number.data):
                created = databases_init.insert_customer(
                    form.person_number.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.email.data,
                    hash_password(form.password.data),
                    form.phone.data,
                    form.address.data
                )
                if created:
                    flash("The user is now registered.", "success")

                    return redirect(url_for("admin_db"))
                else:
                    flash("Can't register the user right now!", "danger")
            else:
                flash("Invalid person number.", "danger")
        else:
            flash("Please fix the highlighted errors.", "warning")

    try:
        all_users = databases_init.show_customers()
    except Exception:
        all_users = {}
    sanitized = {}
    for uid, vals in all_users.items():
        if isinstance(vals, (list, tuple)) and len(vals) >= 11:
            vals = list(vals)
            del vals[4]
            sanitized[uid] = vals
        else:
            sanitized[uid] = vals

    return render_template(
        "admin_db.html",
        title="Admin Dashboard",
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        form=form,
        all_users=sanitized
    )


@app.route('/about')
def about():
    # get lang from URL query string (?lang=swedish), default to english
    lang = request.args.get("lang", "english")
    return render_template('about.html', title='About', lang=lang, translation=read_file_json(translations))

@app.route('/developer')
def developer():
    lang = request.args.get("lang", "english")
    return render_template('developer.html', title='Developer', lang=lang, translation=read_file_json(translations))

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

