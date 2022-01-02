import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # sum of total value of holdnings and cash
    total_value = 0

    # user id for the session
    user_id = session["user_id"]

    # select the portfolio of the user.
    portfolio = db.execute("SELECT * FROM portfolio WHERE userId=?", user_id)

    # looping trough portfolio to get the current value of each holdning, by using the lookup-function.
    # the current value of each symbol is added to the dictionary in portfolio.
    for symbol in portfolio:
        quote_response_index = lookup(symbol['symbol'])
        symbol['price'] = quote_response_index['price']
        total_value = total_value + (symbol['price'] * symbol['shares'])

    # get the amount of cash the user has.
    current_cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)

    # Adding the current cash to the total value.
    total_value = round(total_value + current_cash[0]['cash'], 2)

    # return template index.html to display all the holdnings and current cash balance.
    return render_template("/index.html", portfolio=portfolio, current_cash=round(current_cash[0]['cash'], 2), total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get the symbol and shares of the input from user.
        symbol_buy = request.form.get("symbol")
        shares_buy = request.form.get("shares")

        # if the user failed to choose a stock an error message is displayed.
        if not symbol_buy:
            return apology("A stock must be selected.")

        # check that user input shares
        if not shares_buy:
            return apology("The number of stocks must be selected.")

        # check if shares can be a decimal number.
        if '.' in shares_buy:
            return apology("The number of stocks must be an integer.")

        # try to convert to integer.
        try:
            shares_buy = int(shares_buy)
        except Exception as e:
            return apology("The shares must by an integer!")

        # check that shares is a positive number.
        if shares_buy < 1:
            return apology("The number of shares muct be a positive number.")

        # looking up the company information
        quote_response_buy = lookup(symbol_buy)

        # if the symbol is not found by the lookup-function an apology message is printed.
        if quote_response_buy is None:
            return apology("Could not find a company with this symbol")

        # user id for the session
        user_id = session["user_id"]

        # get the amount of cash the user has
        amount_cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)

        # calculate the purchase cost
        buy_cost = quote_response_buy['price'] * shares_buy

        # check if the user can afford the purchase.
        if buy_cost > amount_cash[0]['cash']:
            return apology("You don't have enough cash to buy these shares.")

        # adding the buy to the db.
        db.execute("INSERT INTO purchase (userId, timestamp, symbol, company, shares, cost) VALUES (?, ?, ?, ?, ?, ?)", user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), quote_response_buy['symbol'], quote_response_buy['name'], shares_buy, buy_cost)


        # uppdating cash for the user in db.
        db.execute("UPDATE users SET cash=? WHERE id=?", (amount_cash[0]['cash'] - buy_cost), user_id)

        # updating portfolio for user in db.
        # selecting all the symbols the user already has in the portfolio.
        user_symbols = db.execute("SELECT symbol FROM portfolio WHERE userId=?", user_id)

        # if it's the users first buy, there is nothing in the portfolio. Thus the new symbol is added.
        if not user_symbols:
            db.execute("INSERT INTO portfolio (userId, symbol, company, shares) VALUES (?, ?, ?, ?)", user_id, quote_response_buy['symbol'], quote_response_buy['name'], shares_buy)

        # if the user has bought stocks before, check if the symbol is already in the portfolio. If it's update the number of shares, else insert the new symbol.
        for symbol in user_symbols:
            if symbol_buy in symbol['symbol']:
                db.execute("UPDATE portfolio SET shares=shares + ? WHERE userId=? AND symbol=?", shares_buy, user_id, quote_response_buy['symbol'])
            else:
                db.execute("INSERT INTO portfolio (userId, symbol, company, shares) VALUES (?, ?, ?, ?)", user_id, quote_response_buy['symbol'], quote_response_buy['name'], shares_buy)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # user id for the session
    user_id = session["user_id"]

    # select the portfolio of the user.
    history = db.execute("SELECT timestamp, symbol, shares, cost FROM purchase UNION SELECT timestamp, symbol, shares, profit as cost FROM sales WHERE userId=? ORDER BY timestamp DESC;", user_id)

    # return template index.html to display all the holdnings and current cash balance.
    return render_template("/history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get the symbol of the input from user.
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("A stock symbol must be selected.")

        # looking up the company information
        quote_response = lookup(symbol)

        if quote_response is None:
            return apology("Could not find a company with this symbol")

        # return a templete with information of the current costs of the stocks.
        return render_template("quoted.html", name=quote_response['name'], price=quote_response['price'], symbol=quote_response['symbol'])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # imports the usernames from sql db.
        usernames = db.execute("SELECT username FROM users")

        # gets the username from form.
        new_username = request.form.get("username")

        # gets the passwords from the two password fields.
        password_reg1 = request.form.get("password")
        password_reg2 = request.form.get("confirmation")

        if not new_username or not password_reg1 or not password_reg2:
            return apology("Username, password and confirmation must be filled in!")

        # if the username is already taken an apology message is returned.
        for user in usernames:
            if new_username in user['username']:
                return apology("The username is already taken. Try with an other username.")
            else:
                continue

        # if the two password dosen't match an apology message is returned.
        if password_reg1 != password_reg2:
            return apology("The passwords dosen't match. Try again.")

        # hash the password before it is saved in the db.
        user_password = generate_password_hash(password_reg1)

        # adding the new user to the db.
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", new_username, user_password)

        # Redirect user to login page.
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # user id for the session
    user_id = session["user_id"]

    # selecting all the symbols the user already has in the portfolio.
    user_symbols = db.execute("SELECT symbol FROM portfolio WHERE userId=?", user_id)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get the symbol and shares of the input from user.
        symbol_sell = request.form.get("symbol")
        shares_sell = request.form.get("shares")

        # if the user failed to choose a stock an error message is displayed.
        if symbol_sell == "Symbol":
            return apology("A stock must be selected.")

        # check that user input shares
        if not shares_sell:
            return apology("The number of stocks must be selected.")

        # check if shares can be a decimal number.
        if '.' in shares_sell:
            return apology("The number of stocks must be an integer.")

         # try to convert to integer.
        try:
            shares_sell = int(shares_sell)
        except Exception as e:
            return apology("The shares must by an integer!")

        # check that shares is a positive number.
        if shares_sell < 1:
            return apology("The number of shares muct be a positive number.")

        # looking up the company information
        quote_response_sell = lookup(symbol_sell)

        # get the amount of shares the user have.
        amount_shares = db.execute("SELECT shares FROM portfolio WHERE userId=? AND symbol=?", user_id, symbol_sell)

        # check if the user can sell the amount of shares
        if shares_sell > amount_shares[0]['shares']:
            return apology("You don't have enough shares to sell these shares.")

        # calculating the profit of the sell
        sell_profit = quote_response_sell['price'] * shares_sell

        # adding the sell to the db.
        db.execute("INSERT INTO sales (userId, timestamp, symbol, company, shares, profit) VALUES (?, ?, ?, ?, ?, ?)", user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), quote_response_sell['symbol'], quote_response_sell['name'], (0-shares_sell), sell_profit)

        # uppdating cash for the user in db.
        db.execute("UPDATE users SET cash=cash + ? WHERE id=?", sell_profit, user_id)

        # updating portfolio for user in db.
        db.execute("UPDATE portfolio SET shares=shares - ? WHERE userId=? AND symbol=?", shares_sell, user_id, quote_response_sell['symbol'])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", user_symbols=user_symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
