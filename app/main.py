from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import create_tables
from .schemas import (
    BorrowerCreate,
    RentalCreate,
    RentalReturn,
    RentalTransfer
)

from .crud import (
    get_all_equipment,
    get_equipment_availability,
    create_borrower,
    create_rental,
    return_rental,
    get_all_rentals,
    transfer_rental
)


app = FastAPI(
    title="AV Room Equipment Rental System",
    description="Equipment booking and rental management system"
)


# Create database tables when application starts
create_tables()


# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/equipment")
def equipment_list():
    return get_all_equipment()


@app.get("/equipment/{equipment_id}/availability")
def equipment_availability(
    equipment_id: int,
    borrow_date: str,
    due_date: str
):
    from datetime import date

    try:
        start = date.fromisoformat(borrow_date)
        end = date.fromisoformat(due_date)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="Due date must be after borrow date"
        )

    result = get_equipment_availability(
        equipment_id,
        start,
        end
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return result


@app.post("/borrowers")
def add_borrower(borrower: BorrowerCreate):

    result = create_borrower(
        borrower.name,
        borrower.email
    )

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Borrower could not be created. Email may already exist."
        )

    return result


@app.post("/rentals")
def add_rental(rental: RentalCreate):

    result = create_rental(
        rental.borrower_id,
        rental.equipment_id,
        rental.quantity,
        rental.borrow_date,
        rental.due_date,
        rental.deposit
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.get("/rentals")
def rental_list():
    return get_all_rentals()


@app.post("/rentals/{rental_id}/return")
def return_equipment(
    rental_id: int,
    rental_return: RentalReturn
):

    result = return_rental(
        rental_id,
        rental_return.return_date
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.post("/rentals/{rental_id}/transfer")
def transfer_equipment(
    rental_id: int,
    transfer: RentalTransfer
):

    result = transfer_rental(
        rental_id,
        transfer.new_borrower_id
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result
