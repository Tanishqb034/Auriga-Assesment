Equipment Rental Management System
Overview

The Equipment Rental Management System is a web application designed for managing the college AV room's equipment lending process.

The system helps the AV room staff track equipment, borrowers, active rentals, availability, returns, deposits, late fees, and transfer of active loans between borrowers.

Features
Add and manage equipment.
Support multiple units of the same equipment.
Register borrowers.
Check equipment availability.
Create equipment rentals.
Set a due date for every rental.
Track active rentals.
Return rented equipment.
Calculate late fees based on overdue days.
Calculate refundable deposit after deducting late fees.
Enforce a borrowing limit for borrowers.
Transfer an active rental from one borrower to another.
Preserve the original due date during a transfer.
Preserve equipment availability during a transfer.
Technology Stack
Python
FastAPI
SQLAlchemy
SQLite
Pydantic
HTML/CSS/JavaScript
Project Structure
equipment_rental/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
│
├── requirements.txt
├── README.md
├── REASONING.md
└── AI_LOGS.md




Setup
1. Clone the repository
git clone <YOUR_PUBLIC_REPOSITORY_URL>
cd equipment_rental
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Run the application
uvicorn app.main:app --reload

The application can then be accessed through the URL shown by the FastAPI server.

FastAPI API documentation is available at:

/docs
Core Business Rules
Equipment Availability

Available equipment is calculated from the total number of units and currently rented units.

An equipment item cannot be rented when sufficient units are unavailable.

Borrowing Limit

A borrower cannot exceed the configured maximum number of active rented items.

Late Fee

Late fee is calculated using:

late_fee = late_days × daily_late_fee
Deposit Refund

The refundable deposit is calculated as:

refund = max(0, deposit - late_fee)
Rental Transfer

An active rental can be transferred from one borrower to another.

During a transfer:

The original rental remains active.
The original due date remains unchanged.
Equipment availability does not change.
The borrower associated with the active rental is updated.
Testing

The following scenarios should be tested before submission:

Create equipment.
Create a borrower.
Rent available equipment.
Attempt to rent unavailable equipment.
Check equipment availability.
Return equipment before the due date.
Return equipment after the due date.
Verify late fee calculation.
Verify deposit refund calculation.
Attempt to exceed the borrowing limit.
Transfer an active rental.
Verify that the due date remains unchanged after transfer.
Verify that equipment availability remains unchanged after transfer.
Debugging

If the application does not start, verify that:

Python is installed.
The virtual environment is activated.
All dependencies are installed.
The command is executed from the project root.
The module path in the uvicorn command matches the project structure.

For API-related issues, use:

/docs

to inspect and test the available endpoints.

Database

The application uses SQLite for local persistence. Database tables are created by the application's database initialization process.

Assumptions

Because the problem statement intentionally leaves some implementation details open, the application uses reasonable assumptions for:

Borrowing limits.
Late-fee calculation.
Deposit handling.
Equipment availability.
Borrower identification.

These assumptions are kept in the application logic and can be changed according to institutional requirements.
