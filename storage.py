import json
import os
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")
def load_high_score():
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as file:
            return int(json.load(file).get("high_score", 0))
    except (OSError, ValueError, TypeError, AttributeError):
        return 0
def save_high_score(score):
    try: 
        with open(SAVE_PATH, "w", encoding="utf-8") as file:
            json.dump({"high_score": int(score)}, file)
    except OSError:
        pass