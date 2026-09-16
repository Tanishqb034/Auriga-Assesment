# Reasoning Behind the Solution

## 1. Understanding the Problem

The college AV room currently uses a paper-based register to manage equipment lending. This makes it difficult to know which equipment is available, who currently has an item, when it is due back, and whether an item has been returned late.

The goal of the application is to provide a simple digital system for managing equipment borrowing, availability, returns, deposits, borrowing limits, and transfers of active loans.

The implementation was prioritized around the core borrowing and return workflow first, followed by deposit handling, limits, and the transfer requirement.

## 2. Main Entities

The system is designed around three main entities:

### Equipment

Equipment represents the gear available in the AV room, such as:

* DSLR cameras
* Projectors
* Microphones
* Tripods

An equipment record can represent multiple units of the same type.

### Borrower

A borrower represents the person or group that takes equipment on rent.

The borrower information is associated with active rentals so that the system can track responsibility for equipment.

### Rental

A rental represents an active or completed borrowing transaction.

It contains information such as:

* Borrower
* Equipment
* Quantity
* Borrow date
* Due date
* Return date
* Deposit
* Late fee
* Rental status
