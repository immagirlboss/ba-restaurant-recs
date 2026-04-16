# BA Eats - Buenos Aires Restaurant Expert System

BA Eats is a restaurant recommendation system for Buenos Aires, powered by a **Prolog** inference engine and a **Flask** web backend. It provides a personalized, dynamic questionnaire to help users find the perfect dining spot based on cuisine, budget, vibe, and more.

## System Overview

The application utilizes a tri-layered architecture:
1.  **Logic Layer (SWI-Prolog)**: A knowledge base (`kb.pl`) containing restaurant facts and logical matching rules.
2.  **Engine Layer (PySWIP + Python)**: A thread-safe bridge (`prolog_engine.py`) that manages user sessions and translates questionnaire answers into Prolog queries.
3.  **Presentation Layer (Flask + Vanilla JS/CSS)**: A web interface that provides a smooth, asynchronous user experience.


**BA Eats** implements a synchronization mechanism using `threading.Lock()` to ensure that every interaction with the Prolog engine is atomic and thread-safe. Each user has an isolated `PrologSession` object that tracks their specific state, while the global lock manages access to the shared logic core.

## Knowledge Representation

### Facts
Restaurants are stored as structured facts:
```prolog
restaurant(Name, Cuisine, Budget, SameArea, Neighborhood, Dietary, Vibe, Distance, Time, Reservation).
```

### Rules & inference
The system uses an inference strategy based on **Unification** and **Constraint Matching**. Instead of simple keyword filtering, the system applies logical rules to determine if a restaurant meets the user's criteria.

