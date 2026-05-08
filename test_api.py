import requests

response = requests.get("http://127.0.0.1:8000/flashcards?topic=Python%20basics&amount=2&level=Beginner")
print("Status:", response.status_code)
print("Response:", response.json())