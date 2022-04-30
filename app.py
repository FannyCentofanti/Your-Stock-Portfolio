import json
from flask import Flask, render_template, redirect, request, session, jsonify, make_response, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from user_data import user_stock_data, get_total_value
from helpers import get_stock_info, login_required, contains, get_display_data

app = Flask(__name__)

app.secret_key = 'BAD_SECRET_KEY'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'URL to database'

db = SQLAlchemy(app)

# setup of the tables in the postgreSQL database to be able to make queries with
#  flask SQLAlchemy.
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(500), unique=True, nullable=False)


class Companies(db.Model):
    __tablename__ = 'companies'
    company_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    industry = db.Column(db.String(128), nullable=False)
    sector = db.Column(db.String(128), nullable=False)


class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.company_id'), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    key = db.Column(db.Integer, primary_key=True)

# global list for display of data for front page and get started.
display_data = []
# global list of user data for the users portfolio.
user_data = []

@app.route("/")
def start():

    # get the data for display table.
    display_data_info = get_display_data()

    #clear display_data list
    display_data.clear()

    # create display_data and convert to json format.
    for data in display_data_info:
        company = user_stock_data(data["symbol"], data["shares"])
        display_data.append(company)

    display_data_json_dump = json.dumps(
        [holding.__dict__ for holding in display_data])
    display_data_json_load = json.loads(display_data_json_dump)

    # calculate the total value of the holdnings in the display portfolio.
    total_value_display = get_total_value(display_data)

    # if someone is logged in var_login is set to true to show a different border.
    if 'user_id' in session:
        return render_template("start.html", var_login=True, display_data=display_data_json_load, total_value_display=total_value_display)
    
    return render_template("start.html", display_data=display_data_json_load, total_value_display=total_value_display)

@app.route("/aboutus/")
def about():

    # if someone is logged in var_login is set to true to show a different border.
    if 'user_id' in session:
        return render_template("aboutus.html", var_login=True)
    
    return render_template("aboutus.html")


@app.route("/getstarted/")
def getstarted():

    # display_data is a global variable and is allready created from the start-page.

    # convert display_data to json format.
    display_data_json_dump = json.dumps(
        [holding.__dict__ for holding in display_data])
    display_data_json_load = json.loads(display_data_json_dump)

    # calculate the total value of the holdnings in the display portfolio.
    total_value_display = get_total_value(display_data)

    # if someone is logged in var_login is set to true to show a different border.
    if 'user_id' in session:
        return render_template("getstarted.html", var_login=True, display_data=display_data_json_load, total_value_display=total_value_display)
    
    return render_template("getstarted.html", display_data=display_data_json_load, total_value_display=total_value_display)


@app.route("/login/", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Forget any user_id
        session.clear()

        # Ensure username was submitted
        if not request.form.get("username"):
            error_message = "Username must be provided."
            return render_template("login.html", error=error_message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error_message = "Password must be provided."
            return render_template("login.html", error=error_message)

        username = request.form.get("username")

        # Query database for username
        rows = Users.query.with_entities(
            Users.id, Users.username, Users.hash).filter_by(username=username).all()

        for user in rows:
            # Ensure username exists and password is correct
            if not user[1] or not check_password_hash(user[2], request.form.get("password")):
                error_message = "Invalid username and/or password"
                return render_template("login.html", error=error_message)

            # Remember which user has logged in
            session["user_id"] = user[0]

        return redirect(url_for('userhome'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", error=None)


@app.route("/logout/")
def logout():
    """Log user out"""

    # clear list of user_data
    user_data.clear()

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register/", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # imports the usernames from sql db.
        usernames = Users.query.with_entities(Users.username).all()

        # gets the username from form.
        new_username = (request.form.get("username")).strip()

        # gets the passwords from the two password fields.
        password_reg1 = (request.form.get("password")).strip()
        password_reg2 = (request.form.get("confirmation")).strip()

        # check that all information was filled in the form.
        if not new_username or not password_reg1 or not password_reg2:
            error_message = "Username, password and confirmation must be filled in!"
            return render_template("register.html", error=error_message)

        # if the username is already taken an apology message is returned.
        for user in usernames:
            if new_username in user['username']:
                error_message = "The username is already taken. Try with an other username."
                return render_template("register.html", error=error_message)
            else:
                continue

        # if the two password dosen't match an apology message is returned.
        if password_reg1 != password_reg2:
            error_message = "The passwords dosen't match. Try again."
            return render_template("register.html", error=error_message)

        # hash the password before it is saved in the db.
        user_password = generate_password_hash(password_reg1)

        # adding the new user to the db
        new_user = Users(username=new_username, hash=user_password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect user to login page.
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/userhome/", methods=["GET"])
@login_required
def userhome():
    """Show portfolio of stocks"""

    userID = session["user_id"]

    # get the portfolio of the user with id == user_id.
    portfolio = Portfolio.query\
        .join(Companies, Portfolio.company_id == Companies.company_id)\
        .add_columns(Companies.symbol, Companies.name, Companies.industry, Companies.sector, Portfolio.shares)\
        .filter(Portfolio.user_id == userID).all()

    # clear global varible list of user_data.
    user_data.clear()

    # create user_data and convert to json format.
    for row in portfolio:
        company = user_stock_data(row[1], row[5])
        user_data.append(company)

    user_data_json_dump = json.dumps(
        [holding.__dict__ for holding in user_data])
    user_data_json_load = json.loads(user_data_json_dump)

    # calculate the total value of the holdnings in the user portfolio.
    total_value_holdnings = get_total_value(user_data)

    return render_template("userhome.html", var_login=True, user_data=user_data_json_load, total_value=total_value_holdnings)


@app.route("/userhome/new-company/", methods=["POST"])
def new_company():
    '''Add a company to the user portfolio'''

    userID = session["user_id"]

    # get data from ajax request
    json_data = request.data
    data = json.loads(json_data)

    # check if JSON data is empty.
    if not data["symbol"]:
        return make_response(json.dumps({"message": "The information for the request is not complete. Please fill in all input fields and try again."}), 400)

    # cast symbol to uppercase letters
    data['symbol'] = data['symbol'].upper()

    # get the ID of the company in db, if it exist
    companyID = Companies.query.filter_by(symbol=data['symbol']).first()

    # if the company is not in the db.
    if companyID == None:

        # add company to db.
        create_company = get_stock_info(data['symbol'])
        if create_company == None:
            return make_response(json.dumps({"message": "Request of stock data faild. Confirm that the symbol is correct and please try again."}), 500)
        
        new_company = Companies(symbol=create_company["symbol"], name=create_company["name"],
                                industry=create_company["industry"], sector=create_company["sector"])
        db.session.add(new_company)
        db.session.commit()

        # update portfolio for user based on the created company_id.
        add_to_portfolio = Portfolio(
            user_id=userID, company_id=new_company.company_id, shares=data['shares'])
        db.session.add(add_to_portfolio)
        db.session.commit()

        # update user_data, total_value_holding with the new company.
        new_user_company = user_stock_data(data['symbol'], data['shares'])
        user_data.append(new_user_company)

        # calculate the total value of the holdnings in the user portfolio.
        total_value_holdnings = get_total_value(user_data)

        # event to use as information in front end
        event = "new"

    # check if the company is a part of the users portfolio.
    elif contains(user_data, lambda x: x.symbol == data['symbol']):
        # update the portfolio of the user.
        Portfolio.query.filter_by(user_id=userID, company_id=companyID.company_id).update(
            dict(shares=(Portfolio.shares + int(data['shares']))))
        db.session.commit()

        # update user_data, total_value_holding with the new company.
        for company in user_data:
            if company.symbol == data['symbol']:
                company.shares += int(data['shares'])
                company.total_value = (company.shares * company.current_stock_value)

        # calculate the total value of the holdnings in the user portfolio.
        total_value_holdnings = get_total_value(user_data)

        # event to use as information in front end
        event = "edit"

    # update portfolio of user based on the companyID.
    else:
        add_to_portfolio = Portfolio(
            user_id=userID, company_id=companyID.company_id, shares=data['shares'])
        db.session.add(add_to_portfolio)
        db.session.commit()

        # update user_data, total_value_holding with the new company.
        new_user_company = user_stock_data(data['symbol'], data['shares'])
        user_data.append(new_user_company)

        # calculate the total value of the holdnings in the user portfolio.
        total_value_holdnings = get_total_value(user_data)

        # event to use as information in front end
        event = "new"

    # get the portfolio of the user with id == user_id.
    portfolio = Portfolio.query\
        .join(Companies, Portfolio.company_id == Companies.company_id)\
        .add_columns(Companies.symbol, Companies.name, Companies.industry, Companies.sector, Portfolio.shares)\
        .filter(Portfolio.user_id == userID).all()
    
    # get the number of companies in the user portfolio.
    nr_companies = len(portfolio)

    # the data which should be returned to the AJAX-request.
    return_json_data = {'event': event, 'user_data': user_data, 'total_value_holdnings': total_value_holdnings, 'nr_companies': nr_companies}

    # return to AJAX-request if everything went well.
    return make_response(json.dumps(return_json_data, default=lambda o: o.encode(), indent=4))


@app.route("/userhome/edit_shares/", methods=["POST"])
def edit_shares():
    '''Edit shares of current holdnings of the user.'''

    userID = session["user_id"]
    event = ""

    # get data from ajax request
    json_data = request.data
    data = json.loads(json_data)

    # check if action was returned from ajax request
    if not data['shares']:
        return make_response(json.dumps({"message": "The information for the request is not complete. Please fill in all input fields and try again."}), 400)

    # cast symbol to uppercase letters
    data['symbol'] = data['symbol'].upper()

    # get the ID of the company in db
    companyID = Companies.query.filter_by(symbol=data['symbol']).first()

    # action add shares to holdning
    if data['action'] == 'Add':

        # update the user_data
        for company in user_data:
            if company.symbol == data['symbol']:
                company.shares += int(data['shares'])
                company.total_value = (company.shares * company.current_stock_value)

        # update the portfolio of the user.
        Portfolio.query.filter_by(user_id=userID, company_id=companyID.company_id).update(
            dict(shares=(Portfolio.shares + int(data['shares']))))
        db.session.commit()

        # calculate the total value of the holdnings in the user portfolio.
        total_value_holdnings = get_total_value(user_data)

        # event to use as information in front end
        event = "edit"

    # action remove share to holdning
    elif data['action'] == 'Remove':

        # update the user_data
        for company in user_data:
            if company.symbol == data['symbol']:
                company.shares -= int(data['shares'])
                company.total_value = (company.shares * company.current_stock_value)

                # check if the number of shares left is zero or less then zero.
                if (company.shares <= 0):
                    # remove the company from portfolio
                    Portfolio.query.filter_by(user_id=userID, company_id=companyID.company_id).delete()
                    db.session.commit()
                    
                    # remove the company from the list user_data.
                    user_data.remove(company)

                    # event to use as information in front end
                    event = "remove"
                else:
                    # update the portfolio of the user.
                    Portfolio.query.filter_by(user_id=userID, company_id=companyID.company_id).update(
                        dict(shares=(Portfolio.shares - int(data['shares']))))
                    db.session.commit()

                    # event to use as information in front end
                    event = "edit"

        # calculate the total value of the holdnings in the user portfolio.
        total_value_holdnings = get_total_value(user_data)

    # someting else went wrong, return error
    else:
        return make_response(json.dumps({"message": "Something went wrong. Please try again."}), 500)

    # get the portfolio of the user with id == user_id.
    portfolio = Portfolio.query\
        .join(Companies, Portfolio.company_id == Companies.company_id)\
        .add_columns(Companies.symbol, Companies.name, Companies.industry, Companies.sector, Portfolio.shares)\
        .filter(Portfolio.user_id == userID).all()
    
    # get the number of companies in the user portfolio.
    nr_companies = len(portfolio)

    # the data which should be returned to the AJAX-request.
    return_json_data = {'event': event, 'user_data': user_data, 'total_value_holdnings': total_value_holdnings, 'nr_companies': nr_companies}

    # return to AJAX-request if everything went well.
    return make_response(json.dumps(return_json_data, default=lambda o: o.encode(), indent=4))
