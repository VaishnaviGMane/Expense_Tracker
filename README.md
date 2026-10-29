# Expense Tracker

A simple web application to manage personal income and expenses. Users
can add transactions, organize them by category, set monthly budgets,
and view financial reports.
Features
- User registration, login, and logout
- Dashboard showing monthly income and expenses
- Add and view income or expense transactions
- Create expense categories
- Set monthly budgets by category
- View reports with charts
- Responsive pages using Bootstrap and custom CSS
Technologies Used
- Python
- Django
- MySQL
- HTML and CSS
- Bootstrap
- Chart.js
Project Structure
expense_tracker/
├── manage.py
├── config/             # Django project settings and main URLs
└── tracker/
    ├── models.py       # Category, Transaction, and Budget models
    ├── forms.py        # Forms for user input
    ├── views.py        # Application logic
    ├── urls.py         # App URL routes
    ├── templates/      # HTML templates
    └── static/         # CSS and other static files


Requirements
- Python
- MySQL Server
- pip
- A web browser
Installation
1. Open the project folder

2. Create a virtual environment

Activate it on Windows:

3. Install packages

4. Create the database

5. Configure the database

6. Run migrations

7. Create an administrator (optional)

8. Start the server
python manage.py runserver
Open the application at:
http://127.0.0.1:8000/

Main Pages
  Page              URL
  Dashboard         /

  Register          /register/
  
  Login             /login/
  
  Transactions      /transactions/
  
  Add Transaction   /transactions/add/
  
  Add Category      /categories/add/
  
  Budgets           /budgets/
  
  Reports           /reports/
  
  Admin             /admin/
  
How to Use
1. Register and log in.
2. Create categories for your transactions.
3. Add income and expense transactions.
4. Set monthly budgets for categories.
5. View the dashboard and reports to review your finances.
