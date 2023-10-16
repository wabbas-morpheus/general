import json
import requests

#applianceURL = morpheus['morpheus']['applianceUrl']
applianceURL = "https://wa-morpheus-54.test.morpheusdata.com"
instName = morpheus['instance']['name']
apiToken = "Bearer "+morpheus['morpheus']['apiAccessToken']

def main():
    another_one = requests.get(
        applianceURL+'/api/instances/',
        headers = {
            "Authorization": apiToken,
            },
        verify = False)
    
    
    
    print(another_one.json())
    

main()
