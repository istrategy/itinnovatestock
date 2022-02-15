import requests

url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes"

querystring = {"region":"ZA","symbols":"ABG"}

headers = {
    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
    'x-rapidapi-key': "6d21b854femsh59624b77de2c787p19b4d9jsn03b898f634f7"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

data= response.text
retStr = data.split(",")
for item in retStr:
    print(item)