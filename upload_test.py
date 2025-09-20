import requests

url = "http://127.0.0.1:5000/upload"
file_path = "uploads/mycalender.ics"
user_id = "12345"

with open(file_path, "rb") as f:
    files = {"ical": f}
    data = {"user_id": user_id}
    response = requests.post(url, files=files, data=data)

print("hello")
print(response.status_code)

