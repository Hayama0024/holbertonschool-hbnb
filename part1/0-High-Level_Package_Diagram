# Task 0: High-Level Package Diagram

## Overview

This document presents the high-level package diagram for the HBnB Evolution application.  
The architecture follows a **three-layer structure**:

1. **Presentation Layer** — Handles user interaction and exposes APIs.  
2. **Business Logic Layer** — Contains core logic and models like User, Place, Review, and Amenity.  
3. **Persistence Layer** — Responsible for data storage, retrieval, and audit logging.

Communication between layers follows the **Facade Pattern**,
where the Presentation Layer interacts with the Business Logic Layer through a simplified interface
(Facade), which in turn accesses the data layer.




## Mermaid Diagram

```mermaid
classDiagram
class PresentationLayer {
    <<interface>>
    + APIService
    + UserInterface
}

class BusinessLogicLayer {
    + User
    + Place
    + Review
    + Amenity
    + FacadeService
}

class PersistenceLayer {
    + DatabaseAccess
    + FileStorage
    + AuditLogger
}

PresentationLayer --> BusinessLogicLayer : uses FacadeService
BusinessLogicLayer --> PersistenceLayer : accesses data




------------------------------------------------------------------------------------------------

### Explanatory Notes

```markdown
## Explanatory Notes

### Presentation Layer
This layer is responsible for all user-facing operations.
It includes:

- `APIService`: Exposes REST APIs for clients.
- `UserInterface`: Provides interaction points for front-end systems or external services.

It communicates with the **FacadeService** in the Business Logic Layer.

-------------------------------------------------------------------------------------------------

### Business Logic Layer
This layer contains the core entities and business logic:

- `User`: Manages user data and roles.
- `Place`: Represents rental properties with details like title, price, and location.
- `Review`: Allows users to leave feedback.
- `Amenity`: Represents features associated with places.
- `FacadeService`: Simplifies access to complex business logic for the presentation layer.

--------------------------------------------------------------------------------------------------

### Persistence Layer
Handles all interactions with the data storage:

- `DatabaseAccess`: Provides CRUD operations for entities.
- `FileStorage`: Handles media and static files.
- `AuditLogger`: Records creation and update timestamps for audit purposes.

---------------------------------------------------------------------------------------------------

### Layer Communication (Facade Pattern)

- The **Presentation Layer** does **not** talk directly to data or models.
- It uses the **FacadeService** as a single access point to core business logic.
- The **Business Logic Layer** then interacts with the **Persistence Layer** to fetch or store data.
- This keeps layers **independent, clean, and maintainable**.
