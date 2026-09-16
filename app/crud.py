from datetime import date
from .database import get_connection


MAX_ITEMS_PER_BORROWER = 5
LATE_FEE_PER_DAY = 50


def get_all_equipment():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM equipment
        ORDER BY id
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_equipment_availability(equipment_id, borrow_date, due_date):
    connection = get_connection()

    equipment = connection.execute("""
        SELECT * FROM equipment
        WHERE id = ?
    """, (equipment_id,)).fetchone()

    if not equipment:
        connection.close()
        return None

    booked = connection.execute("""
        SELECT COALESCE(SUM(quantity), 0) AS booked_quantity
        FROM rentals
        WHERE equipment_id = ?
        AND status = 'ACTIVE'
        AND borrow_date < ?
        AND due_date > ?
    """, (equipment_id, due_date, borrow_date)).fetchone()

    connection.close()

    booked_quantity = booked["booked_quantity"]
    available_quantity = equipment["total_quantity"] - booked_quantity

    return {
        "equipment_id": equipment["id"],
        "name": equipment["name"],
        "total_quantity": equipment["total_quantity"],
        "booked_quantity": booked_quantity,
        "available_quantity": max(0, available_quantity)
    }


def create_borrower(name, email):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO borrowers (name, email)
            VALUES (?, ?)
        """, (name, email))

        connection.commit()

        borrower_id = cursor.lastrowid

        return {
            "id": borrower_id,
            "name": name,
            "email": email
        }

    except Exception:
        return None

    finally:
        connection.close()


def create_rental(
    borrower_id,
    equipment_id,
    quantity,
    borrow_date,
    due_date,
    deposit
):
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}

    if due_date <= borrow_date:
        return {"error": "Due date must be after borrow date"}

    if deposit < 0:
        return {"error": "Deposit cannot be negative"}

    connection = get_connection()

    borrower = connection.execute("""
        SELECT * FROM borrowers
        WHERE id = ?
    """, (borrower_id,)).fetchone()

    if not borrower:
        connection.close()
        return {"error": "Borrower not found"}

    equipment = connection.execute("""
        SELECT * FROM equipment
        WHERE id = ?
    """, (equipment_id,)).fetchone()

    if not equipment:
        connection.close()
        return {"error": "Equipment not found"}

    # Check borrower's currently active items
    current_items = connection.execute("""
        SELECT COALESCE(SUM(quantity), 0) AS total_items
        FROM rentals
        WHERE borrower_id = ?
        AND status = 'ACTIVE'
    """, (borrower_id,)).fetchone()["total_items"]

    if current_items + quantity > MAX_ITEMS_PER_BORROWER:
        connection.close()
        return {
            "error": f"Borrowing limit is {MAX_ITEMS_PER_BORROWER} items"
        }

    # Check equipment availability
    booked = connection.execute("""
        SELECT COALESCE(SUM(quantity), 0) AS booked_quantity
        FROM rentals
        WHERE equipment_id = ?
        AND status = 'ACTIVE'
        AND borrow_date < ?
        AND due_date > ?
    """, (equipment_id, due_date, borrow_date)).fetchone()["booked_quantity"]

    available = equipment["total_quantity"] - booked

    if quantity > available:
        connection.close()
        return {
            "error": f"Only {available} unit(s) available for this period"
        }

    cursor = connection.execute("""
        INSERT INTO rentals (
            borrower_id,
            equipment_id,
            quantity,
            borrow_date,
            due_date,
            deposit
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        borrower_id,
        equipment_id,
        quantity,
        borrow_date.isoformat(),
        due_date.isoformat(),
        deposit
    ))

    connection.commit()

    rental_id = cursor.lastrowid

    connection.close()

    return {
        "id": rental_id,
        "message": "Rental booked successfully"
    }


def return_rental(rental_id, return_date):
    connection = get_connection()

    rental = connection.execute("""
        SELECT * FROM rentals
        WHERE id = ?
    """, (rental_id,)).fetchone()

    if not rental:
        connection.close()
        return {"error": "Rental not found"}

    if rental["status"] == "RETURNED":
        connection.close()
        return {"error": "Rental already returned"}

    due_date = date.fromisoformat(rental["due_date"])

    if return_date < date.fromisoformat(rental["borrow_date"]):
        connection.close()
        return {"error": "Return date cannot be before borrow date"}

    late_days = max(0, (return_date - due_date).days)
    late_fee = late_days * LATE_FEE_PER_DAY

    refund_amount = max(0, rental["deposit"] - late_fee)

    connection.execute("""
        UPDATE rentals
        SET return_date = ?,
            late_fee = ?,
            refund_amount = ?,
            status = 'RETURNED'
        WHERE id = ?
    """, (
        return_date.isoformat(),
        late_fee,
        refund_amount,
        rental_id
    ))

    connection.commit()
    connection.close()

    return {
        "rental_id": rental_id,
        "return_date": return_date.isoformat(),
        "late_days": late_days,
        "late_fee": late_fee,
        "deposit": rental["deposit"],
        "refund_amount": refund_amount,
        "status": "RETURNED"
    }


def get_all_rentals():
    connection = get_connection()

    rows = connection.execute("""
        SELECT
            rentals.*,
            borrowers.name AS borrower_name,
            borrowers.email AS borrower_email,
            equipment.name AS equipment_name
        FROM rentals
        JOIN borrowers ON rentals.borrower_id = borrowers.id
        JOIN equipment ON rentals.equipment_id = equipment.id
        ORDER BY rentals.id DESC
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]

def transfer_rental(rental_id, new_borrower_id):
    connection = get_connection()

    rental = connection.execute("""
        SELECT * FROM rentals
        WHERE id = ?
    """, (rental_id,)).fetchone()

    if not rental:
        connection.close()
        return {"error": "Rental not found"}

    if rental["status"] != "ACTIVE":
        connection.close()
        return {"error": "Only active rentals can be transferred"}

    new_borrower = connection.execute("""
        SELECT * FROM borrowers
        WHERE id = ?
    """, (new_borrower_id,)).fetchone()

    if not new_borrower:
        connection.close()
        return {"error": "New borrower not found"}

    if new_borrower_id == rental["borrower_id"]:
        connection.close()
        return {"error": "Rental is already assigned to this borrower"}

    current_items = connection.execute("""
        SELECT COALESCE(SUM(quantity), 0) AS total_items
        FROM rentals
        WHERE borrower_id = ?
        AND status = 'ACTIVE'
    """, (new_borrower_id,)).fetchone()["total_items"]

    if current_items + rental["quantity"] > MAX_ITEMS_PER_BORROWER:
        connection.close()
        return {
            "error": f"Borrowing limit is {MAX_ITEMS_PER_BORROWER} items"
        }

    old_borrower_id = rental["borrower_id"]

    connection.execute("""
        UPDATE rentals
        SET borrower_id = ?
        WHERE id = ?
    """, (new_borrower_id, rental_id))

    connection.commit()
    connection.close()

    return {
        "rental_id": rental_id,
        "old_borrower_id": old_borrower_id,
        "new_borrower_id": new_borrower_id,
        "due_date": rental["due_date"],
        "quantity": rental["quantity"],
        "message": "Rental transferred successfully"
    }    