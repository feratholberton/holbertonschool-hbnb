# HBnB Documentation

# Introduction to HBnB
This document was created to help understand and implement the HBnB project, a simplified version of AirBnB developed as part of a learning process. Its goal is to clearly explain how the system works, what components it consists of, and how to get it up and running step by step.

HBnB allows the management of data such as users, places to stay, reviews, and more, all through a well-organized structure designed to scale. Throughout this document, you will find information about the tools used, how they connect with each other, and what is needed for everything to work correctly.

The idea is that this guide serves as support both for those working directly on the project and for those who need to understand or maintain it in the future.

# High-Level Package Diagram

```mermaid
classDiagram
class Presentation {
    <<layer>>
    +Services
    +API
}

class Business {
    <<layer>>
    +User
    +Place
    +Review
    +Amenity
}

class Persistence {
    <<layer>>
    +DataAccess
}

Presentation --> Business : Facade
Business --> Persistence : Data Access
```

## Presentation Layer

### Interface between users and the system

Contents:
**Services**: Business-use endpoints (e.g. create user, book place).
**APIs**: HTTP interfaces used by frontend or third-party clients.

## Business Logic Layer

### The main part of the system - business rules, validations and workflows -

Contents:
Core domain **models**: User, Place, Review, Amenity

Business operations: e.g. register_user, add_place, etc.

## Persistence Layer

### Manages how data is stored/retrieved from the database

Contents:
Repositories / DAOs (Data Access Objects)

SQLAlchemy models, ORM mappings, raw queries, etc.

---

## The Facade Pattern

- The Facade Pattern provides a simplified and unified interface (While we work in tasks 0, 1 and 3, the API will be our interface)
- The Presentation Layer talks only to the Facade.
- The Facade delegates work to the Business Logic Layer.

Benefits:
- Reduces coupling between layers.
- Centralizes business flow.
- Makes the interface cleaner and more maintainable.

---

# Detailed Class Diagram for Business Logic Layer

```mermaid
classDiagram

    class BaseModel {
    <<super class>>
    +UUID uuid
    +Date creation_date
    +Date last_update
    }

    class User {
    <<model>>
    +String first_name
    +String last_name
    +String email
    +String password
    +Bool is_admin
    +register()
    +update()
    +delete()
    }

    class Place {
    <<model>>
    +User owner
    +String title
    +String description
    +Number price
    +Number latitude
    +Number longitude
    +List (Amenity) amenities
    +create()
    +update()
    +delete()
    +list()
    }

    class Amenity {
    <<model>>
    +String name
    +String description
    +create()
    +update()
    +delete()
    +list()
    }

    class Review {
    <<model>>
    +String comment
    +Number rating
    +create()
    +update()
    +delete()
    +list()
    }

    User --|> BaseModel : Inheritance
    Place --|> BaseModel : Inheritance
    Amenity --|> BaseModel  : Inheritance
    Review --|> BaseModel : Inheritance

    Place o-- User : Composition
    Place o-- Amenity : Composition
    Place o-- Review : Composition

    User --> Review : Association
```

---
# Detailed Class Diagram for Business Logic Layer
Entities & Relationships
The Business Logic Layer contains the core elements of the application, modeling real-world concepts such as users, places, reviews, and amenities. These entities work together to define the system’s main operations.

## User

Represents a person who interacts with the system.

Has attributes like id, name, and email.

Can create reviews and be associated with places.

## Place

Represents a location within the system.

Includes attributes such as id, name, address, and type.

Is connected to Reviews, which users create.

## Review

Stores a user's opinion about a place.

Includes details like rating, comment, and date.

Is linked to both the User (author of the review) and the Place (place being reviewed).

## Amenity

Represents features or services associated with a place.

Examples include Wi-Fi, Parking, or Accessibility.

Places can have multiple amenities, allowing flexible data management.

## How These Fit Into Business Logic
The Business Logic Layer processes requests and applies system rules. Instead of interacting directly with the database, the entities communicate through well-defined methods and relationships:

User interactions → Users can create, edit, or delete reviews of places.

Place management → Places are created, categorized, and associated with amenities.

Data validation and retrieval → Before saving a review, business rules such as rating and comment validity are verified.

## Facade Pattern
The facade pattern in the business logic layer acts as an intermediary between the presentation layer and business logic. Instead of the presentation layer interacting directly with multiple business components, the facade provides a single point of access. This reduces layer dependencies and simplifies integration.
# Sequence Diagrams for API Calls

## User Registration sequence

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User ->> API : Register User (API Call)
    API -->> API : Wrong Data
    API -->> User : Wrong Data Error Message

    API ->> BusinessLogic : Validate and Process Request
    BusinessLogic -->> BusinessLogic : Validation Failed
    BusinessLogic -->> API : Return Error
    API -->> User : Registration Failed Message

    BusinessLogic ->> Database : Check User Existense
    Database -->> Database : User Already Exist
    Database -->> BusinessLogic : Return Error
    BusinessLogic -->> API : Return Error
    API -->> User : Registration Failed Message

    BusinessLogic ->> Database : Create User
    Database -->> BusinessLogic : Return Success
    BusinessLogic -->> API : Return Success
    API -->> User : Registration Successfully Message
```

---

## Place Creation sequence

```mermaid
sequenceDiagram
  participant User
  participant API
  participant BusinessLogic
  participant DataBase
  
    User ->> API : Place Creation (API Call)
    API -->> API : Wrong Data
    API -->> User : Wrong Data Error Message

    API ->> BusinessLogic : Validate and Process Request
    BusinessLogic -->> BusinessLogic : Validation Failed
    BusinessLogic -->> API : Return Error
    API -->> User : Place Creation Failed Error Message

    BusinessLogic ->> DataBase : Check Place Existense
    DataBase -->> DataBase : Place Already Exist
    DataBase -->> BusinessLogic: Return Error
    BusinessLogic -->> API : Return Error
    API -->> User : Place Creation Failed Error Message

    BusinessLogic ->> DataBase : Create Place
    DataBase -->> BusinessLogic : Place Creation Succesfull
    BusinessLogic -->> API : Return Success
    API -->> User : Successfully Place Creation Message
```

---

## Review Submission sequence

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant DataBase

    User ->> API : Review Submission (API Call)
    API -->> API : Wrong Data
    API -->> User : Wrong Data Error Message

    API ->> BusinessLogic : Validate and Process Request
    BusinessLogic -->> BusinessLogic : Validation Failed
    BusinessLogic -->> API : Return Error
    API -->> User : Review Submission Failed Error Message

    BusinessLogic ->> DataBase : Create Review
    DataBase -->> BusinessLogic : Review Creation Succesfull
    BusinessLogic -->> API : Return Success
    API -->> User : Successfully Review Submission Message
```

---

## Fetching a List of Places sequence

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant DataBase

    User ->> API : Fetching a List of Places (API Call)
    API -->> API : Wrong Data
    API -->> User : Wrong Data Error Message

    API ->> BusinessLogic : Validate and Process Request
    BusinessLogic -->> BusinessLogic : Validation Failed
    BusinessLogic -->> API : Return Error
    API -->> User : Fetching a List of Places <br> Failed Error Message

    BusinessLogic ->> DataBase : Check Places List Existense
    DataBase -->> DataBase : Places List Not Available
    DataBase -->> BusinessLogic: Return Error
    BusinessLogic -->> API : Return Error
    API -->> User : No Places To Show Message

    BusinessLogic ->> DataBase : Get Places List
    DataBase -->> BusinessLogic : Return Places List
    BusinessLogic -->> API : Return Success
    API -->> User : Show Places List
```
