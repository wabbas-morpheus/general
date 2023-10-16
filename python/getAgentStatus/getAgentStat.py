import json
import requests

#applianceURL = morpheus['morpheus']['applianceUrl']
applianceURL = "https://wa-morpheus-54.test.morpheusdata.com"
instID = str(morpheus['instance']['id'])
instName = morpheus['instance']['name']
apiToken = "Bearer "+morpheus['morpheus']['apiAccessToken']

def main():
    another_one = requests.get(
        applianceURL+'/api/instances/'+instID,
        headers = {
            "Authorization": apiToken,
            },
        verify = False)
    
    agentInstalled = another_one.json()['instance']['containerDetails'][0]['server']['agentInstalled']
    
    print('Instance ID = '+instID)
    print('Instance Name = '+instName)
    print('Agent Installed? ='+str(agentInstalled))

main()
