import joblib
import re

def nb_predict(titles: list[str]) -> list[bool]:
    if len(titles) == 0:
        return []
    
    model = joblib.load('suspended.joblib')
    return model.predict(titles)

def regex_predict(titles: list[str]) -> list[bool]:
    keywords = ["class", "suspen", "wala", "pasok", "ill", "heat"]
    def keyword_match(title):
        for kw in keywords:
            if re.search(re.escape(kw), title, re.IGNORECASE):
                return True
        return False

    return [keyword_match(title) for title in titles]

def classify(titles: list[str]) -> dict[str, bool]:
    predictions = zip(titles, nb_predict(titles), regex_predict(titles))
    to_bool = lambda t: True if t == 1 else False
    # model.predict reorders titles; use a dictionary to remap them
    formatted = {
        title: regex_prediction or to_bool(nb_prediction) 
        for (title, nb_prediction, regex_prediction) in predictions
    }

    return formatted

