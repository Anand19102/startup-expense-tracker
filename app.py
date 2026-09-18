from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 

# --- Database Configuration ---
db_config = {
    'host': '127.0.0.1',       
    'user': 'anand',           
    'password': '123@akr', 
    'database': 'startup_expenses'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- ROUTE 1: Fetch the Ledger ---
@app.route('/api/ledger', methods=['GET'])
def get_ledger():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        
        # We now also select the raw IDs so the frontend dropdowns can auto-select the right option during edits
        query = """
            SELECT 
                ExpenseRecord.ExpenseID,
                ExpenseRecord.MemberID,
                ExpenseRecord.ProjectID,
                ExpenseRecord.CategoryID,
                ExpenseRecord.VendorID,
                TeamMember.Name AS Founder, 
                Project.ProjectName,
                Category.CategoryName,
                Vendor.VendorName,
                ExpenseRecord.Description,
                ExpenseRecord.Amount, 
                ExpenseRecord.ExpenseDate 
            FROM ExpenseRecord
            JOIN TeamMember ON ExpenseRecord.MemberID = TeamMember.MemberID
            JOIN Project ON ExpenseRecord.ProjectID = Project.ProjectID
            JOIN Category ON ExpenseRecord.CategoryID = Category.CategoryID
            JOIN Vendor ON ExpenseRecord.VendorID = Vendor.VendorID
            ORDER BY ExpenseRecord.ExpenseDate DESC;
        """
        cursor.execute(query)
        expenses = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return jsonify(expenses), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE 2: Add a New Expense ---
@app.route('/api/add-expense', methods=['POST'])
def add_expense():
    try:
        data = request.json 
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO ExpenseRecord 
            (Amount, ExpenseDate, MemberID, ProjectID, CategoryID, VendorID, Description) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['amount'], data['date'], data['member_id'], 
            data['project_id'], data['category_id'], data['vendor_id'], data['description']
        )
        
        cursor.execute(query, values)
        conn.commit() 
        cursor.close()
        conn.close()
        return jsonify({"message": "Expense added successfully!"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE 3: Delete an Expense ---
@app.route('/api/delete-expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM ExpenseRecord WHERE ExpenseID = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Expense deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE 4: Fetch Dynamic Dropdown Data ---
@app.route('/api/form-data', methods=['GET'])
def get_form_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT MemberID, Name, Role FROM TeamMember")
        members = cursor.fetchall()
        cursor.execute("SELECT ProjectID, ProjectName FROM Project")
        projects = cursor.fetchall()
        cursor.execute("SELECT CategoryID, CategoryName FROM Category")
        categories = cursor.fetchall()
        cursor.execute("SELECT VendorID, VendorName FROM Vendor")
        vendors = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "members": members, "projects": projects,
            "categories": categories, "vendors": vendors
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE 5: Update an Expense (NEW: The Final Lab Requirement) ---
@app.route('/api/update-expense/<int:id>', methods=['PUT'])
def update_expense(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE ExpenseRecord 
            SET Amount = %s, ExpenseDate = %s, MemberID = %s, 
                ProjectID = %s, CategoryID = %s, VendorID = %s, Description = %s
            WHERE ExpenseID = %s
        """
        values = (
            data['amount'], data['date'], data['member_id'], 
            data['project_id'], data['category_id'], data['vendor_id'], 
            data['description'], id
        )
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Expense updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)