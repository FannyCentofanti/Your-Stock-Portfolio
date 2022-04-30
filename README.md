# Your Stock Portfolio
#### Description:
Your Stock Portfolio is a web application. Its purpose is to give the user a possibility to analyze the balance of a stock portfolio with the aspect of the distribution over different sectors. The user registers for an account and adds stock companies and the number of shares. The application fetches stock data via API from IEx Cloud. The percentage of the value of each sector is calculated and the pie chart with the distribution is drawn. The user has the possibility to add new companies to the stock portfolio and edit the number of shares for companies already in the portfolio.
The web application is built according to the Flask framework, using python for backend and HTML, CSS and native Javascript for frontend. The database is a PostgreSQL. Stock data is fetched via API from IEx Cloud. <br />
<br />
The web application is deployed on Heroku: https://yourstockportfolio.herokuapp.com/ <br />
Although the deploy to Heroku introduced some issues in the application that could not be mimicked in the developing environment. Sadly, I was not able to fix these issues. It is seen in the user homepage when the stock portfolio is edited. Sometimes the AJAX-request returns an answer with empty data, and I was not able to understand why.
<br />
To run the web application locally: <br />
- Install libraries in requirements.txt.
- Setup API-key for IEx Cloud.
- Setup PostgreSQL database.
- In terminal run: “python -m flask run”.
## All files
**app.py:** 	The instance of the Flask object, setup of the tables in PostgreSQL database and definitions of all URL routs in the web application. <br />
Tables in PostgreSQL: <br />
- Users: Includes info of all registered users.
- Companies: Includes info of all companies registered to any portfolio.
- Portfolio: Includes the portfolio of each user. <br />
Routs: <br />
- start: Fetches the example stock data and render template of start.html.
- about: Renders template of aboutus.html.
- getstarted: Fetches the example stock data and render template of getstarted.html.
- login: 
    - GET: Render template of login.html.
    - POST: Fetches input from user in form and checks if the input matches the database table Users. 
- logout: Clears session of user and render template of start.html.
- register: 
    - GET: Render template of register.html.
    - POST: Fetches input from user in form and checks if the username if free by looking through the database table Users and checks if the passwords match each other. If everything is ok, render template login.html, else an error message is displayed.
- userhome: Fetches the portfolio of the user from the database table Portfolio and render the template userhome.html.
- new_company: Adds new company to the user’s portfolio. It is initiated trough an AJAX-request.
- edit_shares: Edits the number of shares for a company to the user’s portfolio. It is initiated trough an AJAX-request. <br />
**config.py:**	API key to IEx Cloud. <br />
**helpers.py:** 	Functions for API-request to IEx Cloud stock data, function to apply login required to certain paths, function to search a list for a certain value and function for the example stock data on start.html and getstarted.html. <br />
**industry.py:** 	Specification of the different industries and sectors (not needed to run app, it was used in development). <br />
**Procfile:** 	The file is needed to deploy the web application on Heroku. It specifies the commands that are executed by the app on start-up. <br />
**requirements.txt:** All libraries and modules needed to run the application. <br />
**user_data.py:** 	Class to create stock object for the user portfolio and function to calculate the total current value of the entire user portfolio. <br />
#### static
**diagram_data_structure.json:** Data structure to draw the google pie chart. <br />
**functions.js:** Functions to draw the google pie chart when the page is loaded and resized, function to show modal on user page (when add/remove buttons are clicked), create data to draw google pie chart, AJAX-request when user wants to edit the stock portfolio and functions update the view page based on the changes the user asked for. <br />
**style.css:** Design for some structures in the viewer e.g., sizes of containers, background colours and size of footer. <br />
#### templates
All HTML-files for the project. Bootstrap 5 is used for the design of the web application. Jinja is used to print some of the data received from backend. Google charts is used to draw the pie chart. <br />
- layout.html: HTML layout for all pages on the website.
- aboutus.html: Concise explanation of the purpose of the application.
- getstarted.html: Instructive page to explain how to use the application.
- login.html: Log in page for user.
- logout.html: Logout of user.
- register.html: Page for registration of account.
- start.html: The start page of the web application.
- Userhome.html: The homepage for the user, where he or she can analyze their stock portfolio.
