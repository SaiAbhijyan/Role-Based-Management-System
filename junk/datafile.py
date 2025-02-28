import random
import pandas as pd
import os 

# Define lists of names, designations, states, and zip codes
first_names = ["Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Sophia", "William", "Charlotte",
               "James", "Amelia", "Benjamin", "Isabella", "Lucas", "Mia", "Henry", "Evelyn", "Alexander", "Harper"]
last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
designations = ["Software Engineer", "Cloud Engineer", "Cybersecurity Analyst", "HR Manager", "Product Manager",
                "Financial Analyst", "Operations Manager", "UI/UX Designer", "Marketing Specialist", "Data Scientist",
                "Machine Learning Engineer", "Database Administrator", "IT Support Specialist", "Network Engineer",
                "Legal Consultant", "Customer Success Manager", "QA Engineer", "Technical Lead", "Logistics Coordinator",
                "Solutions Architect"]
states = [
    ("Alabama", "35203"), ("Alaska", "99501"), ("Arizona", "85004"), ("Arkansas", "72201"), ("California", "94103"),
    ("Colorado", "80202"), ("Connecticut", "06103"), ("Delaware", "19904"), ("Florida", "33130"), ("Georgia", "30303"),
    ("Hawaii", "96813"), ("Idaho", "83702"), ("Illinois", "60604"), ("Indiana", "46204"), ("Iowa", "50309"),
    ("Kansas", "66102"), ("Kentucky", "40202"), ("Louisiana", "70130"), ("Maine", "04101"), ("Maryland", "21202"),
    ("Massachusetts", "02109"), ("Michigan", "48226"), ("Minnesota", "55402"), ("Mississippi", "39211"),
    ("Missouri", "63101"), ("Montana", "59601"), ("Nebraska", "68102"), ("Nevada", "89502"), ("New Hampshire", "03301"),
    ("New Jersey", "07102"), ("New Mexico", "87110"), ("New York", "10007"), ("North Carolina", "27601"),
    ("North Dakota", "58102"), ("Ohio", "44101"), ("Oklahoma", "73102"), ("Oregon", "97205"), ("Pennsylvania", "19103"),
    ("Rhode Island", "02903"), ("South Carolina", "29201"), ("South Dakota", "57104"), ("Tennessee", "37219"),
    ("Texas", "78701"), ("Utah", "84102"), ("Vermont", "05601"), ("Virginia", "23220"), ("Washington", "98109"),
    ("West Virginia", "25301"), ("Wisconsin", "53703"), ("Wyoming", "82001")
]

# Define department IDs
departments = [1, 2, 3, 4]  # 1 = IT, 2 = Finance, 3 = Operations, 4 = Software Development

# Generate 500 unique employee records
records = []
for _ in range(500):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    designation = random.choice(designations)
    salary = random.randint(60000, 150000)
    bonus = random.randint(2000, 10000)
    state, zip_code = random.choice(states)
    dep_id = random.choice(departments)
    
    records.append((f"{first_name} {last_name}", designation, salary, bonus, state, zip_code, dep_id))

# Create SQL Insert Statement
sql_statements = """
INSERT INTO payroll.employee (e_name, designation, salary, bonus, state, zip_code, dep_id) VALUES
"""

values = []
for record in records:
    values.append(f"('{record[0]}', '{record[1]}', {record[2]}, {record[3]}, '{record[4]}', '{record[5]}', {record[6]})")

sql_statements += ",\n".join(values) + ";\n"

# Save as SQL file
sql_file_path = os.path(r"C:\MEDRCM\mydata1.sql")
with open(sql_file_path, "w") as f:
    f.write(sql_statements)

# Provide the SQL file for download
sql_file_path
