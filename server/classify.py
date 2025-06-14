import joblib

model = joblib.load('suspended.joblib')
prediction = model.predict(['ayoko na talagang mabuhay', 'wala ngang pasok eh', 'heat index ill students'])
print(prediction)