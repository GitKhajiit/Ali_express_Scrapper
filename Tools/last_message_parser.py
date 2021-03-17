import requests

TOKEN = '1675946307:AAFRDqW-LO-o9FCRriw8YVRu-dO2ZZht2m0'
getUpdates_paramas = {'offset': -1}
response = requests.post(f"https://api.telegram.org/bot{TOKEN}/getUpdates", data=getUpdates_paramas)
message_text = response.json()

print(message_text)
