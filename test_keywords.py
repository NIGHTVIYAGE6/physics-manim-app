import requests

url = 'http://localhost:5000/keywords'
data = {'text': '请展示一个物体自由下落的过程'}

response = requests.post(url, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print("请求失败:", response.status_code)
