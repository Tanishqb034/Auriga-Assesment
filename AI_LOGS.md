Haan, ye Auriga assessment ka AV Room Equipment Lending System lag raha hai. Iska main goal ek backend/API banana hai jisme borrowing, availability, returns, aur twist ke रूप में active loan transfer properly handle ho.

Tumhare prompt ko simple language mein todte hain:

Core requirements
Equipment
DSLR
Projector
Mic
Tripod
Ek item ke multiple units ho sakte hain.
Example: Projector ke 3 units.
Borrower
Student/club/person jo equipment borrow karega.
Borrowing / Loan
Borrower equipment lega.
borrowed_at
due_date
Return hone tak loan active rahega.

Availability
Agar 3 projectors hain aur:

2 borrowed hain
1 available hai

toh system ko clearly batana chahiye:

Projector
Total: 3
Borrowed: 2
Available: 1

Return
Return karte waqt:

actual return date
late days
late fee
deposit refund

calculate hoga.

Deposit
Example:

Deposit = ₹500
Late fee = ₹100

Refund = ₹400

Borrowing limit

Ek borrower unlimited equipment nahi le sakta.

Example:

Maximum active loans = 3

Late fee

Example:

Due date: 10 Sept
Returned: 13 Sept
Late: 3 days

Late fee = 3 × ₹20
         = ₹60
🔥 Twist — sabse important

Assessment ka special requirement hai:

Active loan ko ek borrower se doosre borrower ko transfer karna hai.

Example:

Projector #2

Before:
Borrower = Rahul
Due date = 20 Sept
Status = Active

Transfer:

Rahul → Aman

After:

Borrower = Aman
Due date = 20 Sept
Status = Active
Important:

Due date change nahi hogi.

❌ Wrong:

Rahul → Aman
Due date: 20 Sept → 25 Sept

✅ Correct:

Rahul → Aman
Due date: 20 Sept → 20 Sept

Aur availability bhi change nahi hogi.

Example:

Before transfer:
Projectors = 3
Borrowed = 2
Available = 1

Transfer ke baad:

Projectors = 3
Borrowed = 2
Available = 1

Because equipment physically return nahi hua hai, sirf borrower change hua hai.

API structure bhi roughly aisa ho sakta hai
POST   /borrowers
GET    /equipment
GET    /equipment/{id}/availability

POST   /rentals
POST   /rentals/{id}/return

POST   /rentals/{id}/transfer

Aur transfer request:

{
    "new_borrower_id": 5
}

Response:

{
    "rental_id": 12,
    "old_borrower": 2,
    "new_borrower": 5,
    "due_date": "2026-09-20",
    "status": "active"
}

Tumne jo FastAPI code pehle bheja tha, usme RentalTransfer already bana hua tha:

from .schemas import (
    BorrowerCreate,
    RentalCreate,
    RentalReturn,
    RentalTransfer
)

Iska matlab hum tumhare existing project ko hi assessment ke complete requirements ke according finish kar sakte hain.

Agar tum chaho, main ab tumhare Auriga assessment ke liye complete project ko step-by-step finish karwa deta hoon — database → models → CRUD → FastAPI endpoints → transfer logic → README → reasoning → GitHub/Codespace submission.

help me to buid it

Bilkul. Hum ise step-by-step build karenge, aur goal rahega ki assessment ke liye working, clean FastAPI project ready ho — unnecessary features nahi.

Tumhare previous code se lag raha hai ki tumne already FastAPI + database + schemas + crud structure start kar diya hai. Usi project ko continue karna best rahega.

Architecture
AV Room Lending System
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
│
├── tests/
│   └── test_rentals.py
│
├── requirements.txt
├── README.md
└── reasoning.md
Database entities

Hum initially 3 main tables rakhenge:

Borrower
   │
   │ 1
   │
   │ many
Rental
   │
   │ many
   │
Equipment

Equipment

id
name
category
total_quantity
available_quantity
late_fee_per_day
deposit_amount

Example:

1 | DSLR     | Camera    | 5 | 4 | ₹50 | ₹1000
2 | Projector| Projector | 3 | 2 | ₹30 | ₹500

Borrower

id
name
email

Rental

id
equipment_id
borrower_id
borrowed_at
due_date
returned_at
status
deposit_amount
late_fee
🔥 Transfer logic

This is the part interviewer/assessor will likely check carefully.

Suppose:

Rental #10

Equipment: Projector
Borrower: Rahul
Due date: 20 Sept
Status: ACTIVE

Transfer:

Rahul → Aman

We only change:

borrower_id

We do NOT:

equipment availability
due_date
borrowed_at

So:

Before:
borrower_id = Rahul
due_date = 20 Sept
available = 1

After:
borrower_id = Aman
due_date = 20 Sept
available = 1
Step 1 — Let's inspect your current project

Since you've already started the FastAPI project, don't create everything from scratch yet.

Send me the current contents of these files:

main.py
database.py
models.py
schemas.py
crud.py

You can simply paste them here one by one.

If your structure is:

app/
    main.py
    database.py
    schemas.py
    crud.py

and models.py doesn't exist, that's fine too.

Start by sending database.py and schemas.py. I'll modify your existing code rather than making you rebuild the project.

step by step to build it

Bilkul. Hum zero se step-by-step build karenge, aur har step ke baad tum run karke verify karoge. Isse assessment ke time tumhe code bhi samajh aayega.

Hum FastAPI + SQLite + SQLAlchemy + Pydantic use karenge.

Overall roadmap
STEP 1  → Project setup
STEP 2  → Database setup
STEP 3  → Database models
STEP 4  → Pydantic schemas
STEP 5  → Equipment APIs
STEP 6  → Borrower APIs
STEP 7  → Rental/Borrow API
STEP 8  → Availability
STEP 9  → Return + late fee + deposit
STEP 10 → Borrowing limit
STEP 11 → 🔥 Loan transfer
STEP 12 → Validation + error handling
STEP 13 → Testing
STEP 14 → README + reasoning
STEP 15 → GitHub submission
STEP 1 — Create the project

Create a folder:

auriga-av-room

Open it in VS Code.

Inside it create:

auriga-av-room/
│
├── app/
│
└── requirements.txt

Inside app, create:

app/
├── __init__.py
└── main.py

So currently:

auriga-av-room/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
└── requirements.txt
STEP 2 — Create virtual environment

Open terminal in VS Code:

python -m venv venv

Activate it on Windows PowerShell:

.\venv\Scripts\Activate.ps1

If PowerShell gives an execution-policy error, use:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate again:

.\venv\Scripts\Activate.ps1

You should see something like:

(venv) PS C:\...\auriga-av-room>
STEP 3 — Install packages

Run:

pip install fastapi uvicorn sqlalchemy

Then save dependencies:

pip freeze > requirements.txt
STEP 4 — First FastAPI application

Open:

app/main.py

Put this:

from fastapi import FastAPI

app = FastAPI(
    title="AV Room Equipment Lending System",
    description="Equipment lending and tracking system for college AV room"
)


@app.get("/")
def home():
    return {
        "message": "AV Room Lending System is running"
    }
STEP 5 — Run the server

From the project root:

uvicorn app.main:app --reload

You should get:

Uvicorn running on http://127.0.0.1:8000

Open:

http://127.0.0.1:8000

You should see:

{
    "message": "AV Room Lending System is running"
}
STEP 6 — Check Swagger

This is important for the assessment.

Open:

http://127.0.0.1:8000/docs

You should see:

AV Room Equipment Lending System

and:

GET /

Click GET / → Try it out → Execute.

You should get:

{
  "message": "AV Room Lending System is running"
}
🛑 Stop here

Don't build the database yet.

First make sure Step 1–6 works.

Your terminal should look approximately like:

(venv) PS C:\...\auriga-av-room> uvicorn app.main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000

And /docs should open successfully.

Once this is working, Step 7 will be the database:

SQLite
   ↓
SQLAlchemy
   ↓
Borrower
Equipment
Rental

Then we'll start implementing the actual assessment logic.
