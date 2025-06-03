# HBnB Documentation

# High-Level Package Diagram

```mermaid
---
config:
  theme: redux-dark
  look: neo
---
classDiagram
class Presentation {
  <<layer>>
  +Services
  +API
}
namespace BusinessLayer {
  class Facade {
    <<pattern>>
    +callBusinessLogic()
  }
  class BusinessLogic {
    <<layer>>
    +User
    +Place
    +Review
    +Amenity
  }
}
class Persistence {
  <<layer>>
  +DataAccess
}
Presentation --> Facade : Uses
Facade --> BusinessLogic : Delegates
BusinessLogic --> Persistence : Data Access
```
[**Better View @ mermaidchart.com**](https://www.mermaidchart.com/raw/51c92add-4831-4407-9806-ccf8e186814f?theme=light&version=v0.1&format=svg)

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

- The Facade Pattern provides a simplified and unified interface
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
  +Boolean is_admin
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

%% Python method types: 
%% static method
%% class method
%% instance method

BaseModel --|> User : Inheritance
BaseModel --|> Place : Inheritance
BaseModel --|> Amenity : Inheritance
BaseModel --|> Review : Inheritance
Place o-- User : Composition
Review o-- Place : Composition
Amenity o-- Place : Composition
User --> Review : Association

```

