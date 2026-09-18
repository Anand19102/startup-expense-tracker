# Startup Expense Tracker

**A Full-Stack Financial Web Application for Operational Expense Management**

Startup Expense Tracker is a robust full-stack financial web application engineered with a Python Flask REST API and a normalized MySQL database backend. It enables early-stage ventures to log, categorize, update, and monitor operational costs and founder expenses in real-time through an intuitive dashboard interface.

---

## 🚀 Key Features & Capabilities

* **Complete CRUD Operations:** Full backend support for creating, reading, updating, and deleting financial records dynamically via structured HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
* **Relational Data Integrity:** Maps transactional data accurately across multiple relational entities (`TeamMember`, `Project`, `Category`, `Vendor`).
* **Dynamic Form Data API:** Automatically populates frontend dropdown options by querying database tables in real-time.
* **RESTful JSON Architecture:** Utilizes Flask and `flask-cors` to maintain seamless, asynchronous communication between the server and frontend interface.

---

## 🛠 Technology Stack

* **Frontend:** HTML5, CSS3, JavaScript, Responsive UI Components
* **Backend:** Python, Flask, Flask-CORS
* **Database:** MySQL Server (`mysql-connector-python`)
* **Environment & Tools:** Python Virtual Environment (`venv`), Git, GitHub, Postman (for API endpoint testing)

---

## 📊 Database Schema Overview

The application is powered by a normalized relational database (`startup_expenses`) configured with foreign key constraints to maintain strict relational integrity:

* **`ExpenseRecord`:** The central transactional ledger logging transaction amounts, dates, descriptions, and foreign keys referencing team members, projects, categories, and vendors.
* **`TeamMember`:** Stores founder and team member identities along with their operational roles (`MemberID`, `Name`, `Role`).
* **`Project`:** Tracks active startup initiatives and project names (`ProjectID`, `ProjectName`).
* **`Category`:** Classifies financial outlays into distinct operational sectors (`CategoryID`, `CategoryName`).
* **`Vendor`:** Maintains records of external suppliers and service providers (`VendorID`, `VendorName`).

---

## ⚙️ Installation & Local Execution

### 1. Clone the Repository
```bash
git clone [https://github.com/Anand19102/startup-expense-tracker.git](https://github.com/Anand19102/startup-expense-tracker.git)
cd startup-expense-tracker
```

### 2. Set Up the Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask flask-cors mysql-connector-python
```

### 4. Configure Database & Run
1. Ensure your local MySQL server is running and provision the `startup_expenses` database with the required schema and relational tables.
2. Verify your database configuration credentials in `app.py`:
   ```python
   db_config = {
       'host': '127.0.0.1',       
       'user': 'anand',           
       'password': 'your_password',  
       'database': 'startup_expenses'
   }
   ```
3. Start the Flask application server:
   ```bash
   python app.py
   ```
The backend API service will run locally at `http://127.0.0.1:5000`.

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/ledger` | `GET` | Fetches the complete expense ledger joined across all related entity tables, sorted by date. |
| `/api/add-expense` | `POST` | Inserts a new financial record into the database ledger. |
| `/api/update-expense/<id>` | `PUT` | Updates an existing expense record by its unique ID. |
| `/api/delete-expense/<id>` | `DELETE` | Removes a specific expense record from the ledger. |
| `/api/form-data` | `GET` | Retrieves dynamic dropdown options for members, projects, categories, and vendors. |
