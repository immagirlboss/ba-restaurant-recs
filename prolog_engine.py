import threading
from pyswip import Prolog

# Global lock for PySWIP since the underlying SWI-Prolog engine 
# accessed via foreign interface is not natively thread-safe for concurrent queries.
prolog_lock = threading.Lock()
prolog = Prolog()
prolog.consult("kb.pl")

class PrologSession:
    """
    Manages a single user's interaction with the Prolog engine.
    Stores session answers and determines the next question.
    """
    
    QUESTIONS = [
        {
            "id": "cuisine",
            "text": "What type of cuisine are you in the mood for?",
            "options": [
                "argentine", "italian", "asian", "cafe", "dessert", 
                "empanadas", "street_food", "fast_food", "any"
            ]
        },
        {
            "id": "budget",
            "text": "What is your budget range?",
            "options": ["low", "medium", "high", "luxury", "any"]
        },
        {
            "id": "same_area",
            "text": "Are you looking for something near the Res Hall (Centro/Retiro)?",
            "options": ["yes", "no"]
        },
        {
            "id": "neighborhood",
            "text": "Which neighborhood are you in or heading to?",
            "options": ["centro", "retiro", "palermo", "san_telmo", "recoleta"],
            "condition": lambda answers: answers.get("same_area") == "no"
        },
        {
            "id": "dietary",
            "text": "Any dietary preferences or restrictions?",
            "options": ["none", "vegetarian", "vegan", "celiac", "halal", "any"]
        },
        {
            "id": "vibe",
            "text": "What kind of vibe are you looking for?",
            "options": ["casual", "romantic", "family", "trendy", "any"]
        },
        {
            "id": "distance",
            "text": "How far are you willing to travel?",
            "options": ["walking", "short_uber", "any"],
            "condition": lambda answers: answers.get("same_area") == "yes"
        },
        {
            "id": "time_pref",
            "text": "What time is it or when do you plan to eat?",
            "options": ["breakfast", "lunch", "dinner", "late_night", "any"]
        },
        {
            "id": "reservation_pref",
            "text": "Do you have a reservation preference?",
            "options": ["yes", "no", "no_preference"]
        }
    ]

    def __init__(self):
        self.answers = {}
        self.current_question_index = 0

    def get_next_question(self):
        """Returns the next relevant question based on previous answers."""
        while self.current_question_index < len(self.QUESTIONS):
            q = self.QUESTIONS[self.current_question_index]
            # Check if this question has a condition and if it's met
            if "condition" in q:
                if not q["condition"](self.answers):
                    self.current_question_index += 1
                    continue
            
            # Return a cleaned copy for JSON serialization (no functions)
            q_clean = q.copy()
            if "condition" in q_clean:
                del q_clean["condition"]
            return q_clean
        return None

    def submit_answer(self, question_id, answer):
        """Stores the answer and advances the state."""
        self.answers[question_id] = answer
        self.current_question_index += 1

    def recommend(self):
        """
        Executes the Prolog query with the collected answers.
        Uses a thread lock to ensure safe access to the shared interpreter.
        """
        # Prepare defaults for neighborhood if same_area was yes
        neighborhood = self.answers.get("neighborhood", "any")
        if self.answers.get("same_area") == "yes":
            neighborhood = "any" # In our KB, same_area=yes matches RSameArea=yes regardless of NBH

        # Construct the query string
        # recommend(Name, UNbh, UCuis, UBudg, USame, UDiet, UVibe, UDist, UTime, URes)
        query_str = (
            f"recommend(Name, "
            f"'{neighborhood}', "
            f"'{self.answers.get('cuisine', 'any')}', "
            f"'{self.answers.get('budget', 'any')}', "
            f"'{self.answers.get('same_area', 'no')}', "
            f"'{self.answers.get('dietary', 'any')}', "
            f"'{self.answers.get('vibe', 'any')}', "
            f"'{self.answers.get('distance', 'any')}', "
            f"'{self.answers.get('time_pref', 'any')}', "
            f"'{self.answers.get('reservation_pref', 'no_preference')}')"
        )

        results = []
        with prolog_lock:
            try:
                # Query returning all matching Name values
                q = prolog.query(query_str)
                for res in q:
                    results.append(res["Name"])
                q.close()
            except Exception as e:
                print(f"Prolog Query Error: {e}")
        
        return self._format_results(results)

    def _format_results(self, names):
        """Enriches the restaurant names with more data from the KB."""
        formatted = []
        with prolog_lock:
            for name in names:
                # Get full fact to display card details
                # restaurant(Name, Cuisine, Budget, SameArea, Neighborhood, Dietary, Vibe, Distance, Time, Reservation)
                q = prolog.query(f"restaurant('{name}', C, B, S, N, D, V, Dist, T, R)")
                for r in q:
                    formatted.append({
                        "name": name.replace("_", " ").title(),
                        "cuisine": str(r["C"]),
                        "budget": str(r["B"]),
                        "neighborhood": str(r["N"]).title(),
                        "vibe": str(r["V"]),
                        "tags": [str(r["C"]), str(r["B"]), str(r["V"])]
                    })
                q.close()
        return formatted