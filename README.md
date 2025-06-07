# HBnB Documentation

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

# Sequence Diagrams for API Calls

## User Registration sequence

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User ->> API : Register User (API Call)
API ->> BusinessLogic : Validate and Process Request
BusinessLogic -->> BusinessLogic : Validation Failed
BusinessLogic -->> API : Return Error
API -->> User : Registration Failed Message

BusinessLogic ->> Database : Check User Existense
Database -->> Database : User Already Exist
Database -->> BusinessLogic : Return Error
BusinessLogic -->> API : Return Error
API -->> User : Registration Failed Message

BusinessLogic ->> Database : Save Data
Database -->> BusinessLogic : Confirm Save
BusinessLogic -->> API : Return Success
API -->> User : Registration Successfully Message
```

---

## Place Creation sequence

```mermaid
sequenceDiagram
  participant User as User
  participant API as API
  participant BusinessLogic as BusinessLogic
  participant DataBase as DataBase
  User ->> API: Creacion de lugar
  API -->> User: Mensaje Error de Datos 
  API ->> BusinessLogic: Valida y Procesa los datos del lugar
  BusinessLogic -->> API: Datos incorrectos
  BusinessLogic ->> DataBase: Valida que no exista y Guarda
  DataBase -->> BusinessLogic: Se guardo exitosamente
  BusinessLogic -->> API: Se guardo correctamente
  API -->> User: Mensaje de exito, codigo 201
  DataBase -->> BusinessLogic: Error, ya existe ese lugar
  BusinessLogic -->> API: El lugar ya existe
  API -->> User: Mensaje de error, codigo 404

```

---

## Review Submission sequence

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Envia la reseña
API->>BusinessLogic: Valida la reseña
BusinessLogic -->> API: Reseña invalida codigo 404
API -->> User: Mensaje de error 
BusinessLogic ->> Database: Guarda la reseña
Database-->>BusinessLogic: Se guardo correctamente 
BusinessLogic-->>API: Quedo creada con exito, codigo 201 
API-->>User: Mensaje de exito 
```

---

## Fetching a List of Places sequence

```mermaid
sequenceDiagram
  participant User as User
  participant API as API
  participant BusinessLogic as BusinessLogic
  participant Database as Database

  User ->> API: El usuario pide una lista de lugares 
  API ->> BusinessLogic: Analiza y valida los parametros
  BusinessLogic -->> API: Analisis y validacion incorrecto
  API -->> User: Mensaje de error
  BusinessLogic ->> Database: Consulta si existen los lugares
  Database -->> BusinessLogic: Existen
  BusinessLogic -->> API: Existen correctamente
  API -->> User: Mensaje de exito
  Database -->> BusinessLogic: No existen
  BusinessLogic -->> API: No encontrado
  API -->> User: Mensaje de No encontrado
```
