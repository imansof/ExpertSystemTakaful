#to see database content

import sqlite3


def view_all_data():
   conn = sqlite3.connect('takaful_users.db')
   cursor = conn.cursor()


   print("=== USERS TABLE ===")
   cursor.execute("SELECT * FROM users")
   users = cursor.fetchall()
   for row in users:
       print(row)


   print("\n=== USER INPUT TABLE ===")
   cursor.execute("SELECT * FROM user_input")
   inputs = cursor.fetchall()
   for row in inputs:
       print(row)


   conn.close()


view_all_data()
