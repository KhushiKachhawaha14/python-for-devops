import requests

api_url = "https://jsonplaceholder.typicode.com/todos/1" # server URL (API)

response = requests.get(url=api_url)
print(response.json())

for key,value in response.json().items():
    print(key,value)
    # if key == "userId":
    #     if value in [1,200,300]:
    #         print("User found")