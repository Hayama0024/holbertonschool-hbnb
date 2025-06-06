# HBnB Evolution - Technical Documentation

This repository contains the **complete technical architecture** and design documentation for the HBnB Evolution application. HBnB is a simplified AirBnB-like system enabling users to manage listings (places), reviews, and amenities.

The project follows a **clean layered architecture** with strict separation of concerns and is documented through a series of UML diagrams and supporting explanations.

---

## 📁 Directory Structure

```
part1/
├── task-0.pdf                  # High-Level Package Diagram
├── task-1.pdf                  # Class Diagram (Business Logic Layer)
├── task-2 diag 4.1.pdf         # Sequence Diagram: User Registration
├── task-2 diag 4.2.pdf         # Sequence Diagram: Place Creation
├── task-2 diag 4.3.pdf         # Sequence Diagram: Review Submission
├── task-2 diag 4.4.pdf         # Sequence Diagram: Fetching Places
└── HBnB Project - Comprehensive Technical Documentation.pdf
```

---

## 🧱 High-Level Package Diagram (task-0.pdf)

This diagram presents the layered architecture of HBnB:

* **Presentation Layer**: Handles API requests (e.g., `UserController`, `PlaceController`, `ReviewController`).
* **Facade Layer**: Implements the **Facade Pattern**, abstracting business logic (e.g., `UserFacade`).
* **Business Logic Layer**: Core services and domain logic (`UserService`, `PlaceService`, etc.).
* **Persistence Layer**: Responsible for database interaction through repositories (`UserRepository`, etc.).

> The facade layer cleanly decouples the presentation and business logic, promoting maintainability.

---

## 🧠 Class Diagram: Business Logic Layer (task-1.pdf)

This class diagram models the core entities and their relationships:

### Entities:

* **User**: Includes name, email, password, admin flag.
* **Place**: Contains title, description, price, lat/lon, and links to User and Amenity.
* **Review**: Includes rating, comment, and links to Place and User.
* **Amenity**: Describes features (e.g., WiFi, parking).

### Relationships:

* A `User` **owns** many `Places`
* A `User` **writes** many `Reviews`
* A `Place` **has** many `Reviews` and **contains** many `Amenities`

All entities use `UUID` as primary identifiers and track `created_at`/`updated_at` fields for auditability.

---

## 🔄 Sequence Diagrams: API Use Cases

### 1. 👤 User Registration (task-2 diag 4.1.pdf)

Flow:

* `POST /users {"email":..., "password":...}`
* API passes data to Business Logic (`create_user()`)
* DB insert is performed → response returned

### 2. �� Place Creation (task-2 diag 4.2.pdf)

Flow:

* `POST /places {...}`
* API calls `create_place(user_id, data)`
* DB saves the place → result is returned to user

### 3. 📝 Review Submission (task-2 diag 4.3.pdf)

Flow:

* `POST /review {...}`
* Business logic saves review via `create_review()`
* DB insert and success response to user

### 4. 📍 Fetching Place List (task-2 diag 4.4.pdf)

Flow:

* `GET /place?city=Albi`
* API calls `get_place_by_city("Albi")`
* SQL query returns matched places → JSON response to client

---

## 📘 Comprehensive Document (task-3)

All diagrams and explanations above are compiled in one reference file:

* [`HBnB Project - Comprehensive Technical Documentation.pdf`](./part1/HBnB%20Project%20-%20Comprehensive%20Technical%20Documentation.pdf)

This document was prepared to support architecture design, implementation planning, and team onboarding.

---

## ✅ Summary

* ✅ Clear 3-Layer (plus Facade) architecture
* ✅ SOLID-compliant entity design with UUID and timestamps
* ✅ Well-documented API behaviors with real-world sequence flows

> This technical documentation enables the implementation of HBnB with clarity, maintainability, and architectural consistency.

