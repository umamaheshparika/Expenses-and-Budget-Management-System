# Expenses & Budget Management System

A web-based application for recording personal expenses and managing monthly budgets. The project is built with **Python**, **FastAPI**, **SQLAlchemy**, **SQLite**, and **HTML/CSS templates rendered with Jinja2**.

## Features

### Expense management
- Add an expense with its name, amount, payment method, and description.
- View all recorded expenses.
- Update and delete expenses.
- View expenses sorted by amount.
- Filter expenses by payment method.
- View expense totals month by month.
- View the individual expenses recorded for a selected month.

### Budget management
- Add a budget for a month and year.
- View all budgets.
- Update and delete a budget.
- View the budget amount, total expenses, and remaining amount for each budget.

## Technologies

- **Backend:** Python, FastAPI
- **Database ORM:** SQLAlchemy
- **Database:** SQLite (`financial.db`)
- **Frontend:** HTML and CSS
- **Templating:** Jinja2
- **Server:** Uvicorn

## Project structure

```text
EXPENSES-BUDGET-MANAGEMENT/
├── main.py
├── databse.py
├── financial.db
├── requirements.txt
├── README.md
└── templates/
    ├── main_home_page.html
    ├── home.html
    ├── bud_home.html
    ├── form.html
    ├── view_all.html
    ├── update_form.html
    ├── view_by_amount.html
    ├── show_methods.html
    ├── view_by_method.html
    ├── month_wise_exp.html
    ├── date_wise_exps.html
    ├── budget_form.html
    ├── view_all_budgets.html
    ├── edit_budgt_form.html
    └── remaining_budget.html
```

## Setup and installation

1. Install Python (3.10 or newer recommended).
2. Open a terminal in the project directory.
3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment.

   **Windows (Command Prompt):**

   ```bat
   venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   source venv/bin/activate
   ```

5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Run the application

From the project directory, run:

```bash
uvicorn main:app --reload
```

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

The application uses the SQLite database file `financial.db` in the project directory. The SQLAlchemy models in `main.py` create the database tables when the application starts (through `Base.metadata.create_all`).

## Main application routes

| Route | Purpose |
|---|---|
| `/` | Main home page |
| `/exp` | Expense home page |
| `/exp/add` | Add an expense |
| `/exp/all` | View all expenses |
| `/exp/update/{exp_id}` | Edit an expense |
| `/exp/by/amount` | View expenses ordered by amount |
| `/exp/by/method` | Choose a payment method to filter by |
| `/exp/by/{method}` | View expenses for a payment method |
| `/exp/month` | View monthly expense totals |
| `/exp/{month}` | View expenses for a month (`YYYY-MM`) |
| `/bud` | Budget home page |
| `/add/budget` | Add a budget |
| `/view/budget` | View all budgets |
| `/budget/edit/{budgt_id}` | Edit a budget |
| `/budget/remaining` | View budget usage and remaining amounts |

Expense and budget deletion are handled by POST routes `/exp/delete/{exp_id}` and `/budget/delete/{budgt_id}`.

## Notes

- The database connection is configured for SQLite using `sqlite:///./financial.db`.
- Monthly expense grouping uses SQLite's `strftime` function.
- The expense and update HTML forms include a budget selector. However, the current POST handlers in `main.py` do not read or assign the submitted `budget_id`. Therefore, selecting a budget in those forms does not currently associate the saved or updated expense with that budget. The remaining-budget calculation relies on this association, so this backend handling needs to be completed for the calculation to reflect those expenses correctly.
- `databse.py` is present in the project archive but is currently empty; the database setup and models are defined in `main.py`.
