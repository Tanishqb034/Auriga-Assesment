const API = "";


// ===============================
// Load Equipment
// ===============================

async function loadEquipment() {
    try {
        const response = await fetch(`${API}/equipment`);

        if (!response.ok) {
            throw new Error("Failed to load equipment");
        }

        const equipment = await response.json();

        const list = document.getElementById("equipment-list");
        const availabilitySelect = document.getElementById("availability-equipment");
        const bookingSelect = document.getElementById("booking-equipment");

        list.innerHTML = "";
        availabilitySelect.innerHTML = "";
        bookingSelect.innerHTML = "";

        equipment.forEach(item => {

            // Equipment card
            const card = document.createElement("div");
            card.className = "equipment-card";

            card.innerHTML = `
                <h3>${item.name}</h3>
                <p><strong>Category:</strong> ${item.category}</p>
                <p><strong>Total Units:</strong> ${item.total_quantity}</p>
            `;

            list.appendChild(card);


            // Availability dropdown
            const availabilityOption = document.createElement("option");

            availabilityOption.value = item.id;
            availabilityOption.textContent =
                `${item.name} (${item.total_quantity} units)`;

            availabilitySelect.appendChild(availabilityOption);


            // Booking dropdown
            const bookingOption = document.createElement("option");

            bookingOption.value = item.id;
            bookingOption.textContent = item.name;

            bookingSelect.appendChild(bookingOption);
        });

    } catch (error) {
        console.error(error);

        document.getElementById("equipment-list").innerHTML =
            "<p>Unable to load equipment.</p>";
    }
}



// ===============================
// Check Availability
// ===============================

async function checkAvailability() {

    const equipmentId =
        document.getElementById("availability-equipment").value;

    const borrowDate =
        document.getElementById("availability-borrow-date").value;

    const dueDate =
        document.getElementById("availability-due-date").value;

    const result =
        document.getElementById("availability-result");


    if (!borrowDate || !dueDate) {
        result.textContent = "Please select both dates.";
        return;
    }


    try {

        const response = await fetch(
            `${API}/equipment/${equipmentId}/availability` +
            `?borrow_date=${borrowDate}&due_date=${dueDate}`
        );


        const data = await response.json();


        if (!response.ok) {
            result.textContent =
                data.detail || "Unable to check availability.";

            return;
        }


        result.innerHTML = `
            <div class="rental-card">
                <p><strong>Equipment:</strong> ${data.name}</p>
                <p><strong>Total Units:</strong> ${data.total_quantity}</p>
                <p><strong>Booked:</strong> ${data.booked_quantity}</p>
                <p><strong>Available:</strong> ${data.available_quantity}</p>
            </div>
        `;

    } catch (error) {

        result.textContent =
            "Unable to connect to server.";

        console.error(error);
    }
}



// ===============================
// Add Borrower
// ===============================

async function addBorrower() {

    const name =
        document.getElementById("borrower-name").value.trim();

    const email =
        document.getElementById("borrower-email").value.trim();

    const result =
        document.getElementById("borrower-result");


    if (!name || !email) {
        result.textContent =
            "Please enter name and email.";

        return;
    }


    try {

        const response = await fetch(
            `${API}/borrowers`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            result.textContent =
                data.detail || "Unable to create borrower.";

            return;
        }


        result.textContent =
            `Borrower created successfully. ID: ${data.id}`;


        document.getElementById("borrower-name").value = "";
        document.getElementById("borrower-email").value = "";

    } catch (error) {

        result.textContent =
            "Unable to connect to server.";

        console.error(error);
    }
}



// ===============================
// Create Booking
// ===============================

async function createBooking() {

    const borrowerId =
        Number(document.getElementById("booking-borrower").value);

    const equipmentId =
        Number(document.getElementById("booking-equipment").value);

    const quantity =
        Number(document.getElementById("booking-quantity").value);

    const borrowDate =
        document.getElementById("booking-borrow-date").value;

    const dueDate =
        document.getElementById("booking-due-date").value;

    const deposit =
        Number(document.getElementById("booking-deposit").value);


    const result =
        document.getElementById("booking-result");


    if (
        !borrowerId ||
        !equipmentId ||
        !quantity ||
        !borrowDate ||
        !dueDate ||
        deposit < 0
    ) {
        result.textContent =
            "Please fill all booking fields correctly.";

        return;
    }


    try {

        const response = await fetch(
            `${API}/rentals`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    borrower_id: borrowerId,

                    equipment_id: equipmentId,

                    quantity: quantity,

                    borrow_date: borrowDate,

                    due_date: dueDate,

                    deposit: deposit
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            result.textContent =
                data.detail || "Booking failed.";

            return;
        }


        result.textContent =
            `Booking successful. Rental ID: ${data.id}`;


        loadRentals();

    } catch (error) {

        result.textContent =
            "Unable to connect to server.";

        console.error(error);
    }
}



// ===============================
// Load Rentals
// ===============================

async function loadRentals() {

    const list =
        document.getElementById("rentals-list");


    try {

        const response =
            await fetch(`${API}/rentals`);


        const rentals =
            await response.json();


        list.innerHTML = "";


        if (rentals.length === 0) {

            list.innerHTML =
                "<p>No rentals found.</p>";

            return;
        }


        rentals.forEach(rental => {

            const card =
                document.createElement("div");

            card.className =
                "rental-card";


            card.innerHTML = `
                <p><strong>Rental ID:</strong> ${rental.id}</p>

                <p><strong>Borrower:</strong>
                    ${rental.borrower_name}
                </p>

                <p><strong>Equipment:</strong>
                    ${rental.equipment_name}
                </p>

                <p><strong>Quantity:</strong>
                    ${rental.quantity}
                </p>

                <p><strong>Borrow Date:</strong>
                    ${rental.borrow_date}
                </p>

                <p><strong>Due Date:</strong>
                    ${rental.due_date}
                </p>

                <p><strong>Status:</strong>
                    ${rental.status}
                </p>

                <p><strong>Deposit:</strong>
                    ₹${rental.deposit}
                </p>
            `;


            list.appendChild(card);

        });

    } catch (error) {

        list.innerHTML =
            "<p>Unable to load rentals.</p>";

        console.error(error);
    }
}



// ===============================
// Initial Load
// ===============================

loadEquipment();

loadRentals();