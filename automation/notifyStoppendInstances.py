#Author Waqas Abbas Oct 2023

import smtplib, ssl
import json
import requests
import sys
from datetime import datetime,date
from morpheuscypher import Cypher
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

shutdownDays = 1
listOfInstOverTimeLimt = []
port = 587  # For starttls
smtp_server = "smtp.office365.com"
sender_email = "myemail@outlook.com"


applianceURL = morpheus['morpheus']['applianceUrl']
apiToken = "Bearer "+morpheus['morpheus']['apiAccessToken']

#Get email password from Morpheus Cypher
c = Cypher(url=applianceURL,morpheus=morpheus,ssl_verify=False)
email_password=c.get("secret/mypass000")





def getServers():
    response = requests.get(
        applianceURL+'/api/servers/?max=100000',
        headers = {
            "Authorization": apiToken,
            },
        verify = False)
    servers = response.json()['servers']
    return servers

def getInstances():
    response = requests.get(
        applianceURL+'/api/instances/?max=10000',
        headers = {
            "Authorization": apiToken,
            },
        verify = False)
    return response.json()['instances']


def getUsers():
    response = requests.get(
        applianceURL+'/api/users/?max=1000',
        headers = {
            "Authorization": apiToken,
            },
        verify = False)
    return response.json()['users']


def getServerWithId(sid,servers):
    for s in servers:
        if s['id']==sid:
            return s

def getUserWithId(uid,users):
    for u in users:
        if u['id']==uid:
            return u

def formatInstanceForEmail(i):


    inst = ""
    message= """\
Subject: Instance {instanceName} has been offline for over {shutdownDays} days

Instance {instanceName} has been offline for over {shutdownDays} days:

<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>


""".format(shutdownDays=shutdownDays,instanceName=i['instanceName'])

    inst = message
    sNames=''
    inst = inst +('Instance ID = '+str(i['id'])+'\nInstance Name = '+i['instanceName']+'\nTenant = '+i['tenant']['name']+'\nCloud = '+i['cloud']['name']+'\nPrice = '+str(i['price']['price'])+' per '+i['price']['unit']+'\nVMs = ')
    for s in i['servers']:
        sNames = sNames + s['serverName'] +', '

    inst = inst + sNames.rstrip(", ")+'\n\n\n'
    html = MIMEText(inst, "html")
    return html

def getOfflineInstances():
    morphInstances = getInstances()# Get instances/servers from morpheus api
    morphServers = getServers()
    morphUsers = getUsers()
    for i in morphInstances:
        print(i['name'])
        instanceID = i['id']
        instanceName = i['name']
        tenant = i['tenant']
        cloud = i['cloud']
        servers = i['servers']
        instancePrice = i['instancePrice']
        owner = getUserWithId(i['owner']['id'],morphUsers)
        offServers = []
        for s in servers: #get details about the servers that belong to each instance
            serverDetails = getServerWithId(s,morphServers)
            serverPowerState = serverDetails['powerState']
            if serverPowerState=="off":
               offServers.append({'serverId':serverDetails['id'],'serverName':serverDetails['name']}) 
        instanceLastUpdatedDate = i['lastUpdated']

        if instanceLastUpdatedDate:
            today = datetime.now()
            datetime_object = datetime.strptime(instanceLastUpdatedDate, '%Y-%m-%dT%H:%M:%SZ')
            delta = today - datetime_object


            print(datetime_object)  # printed in default format
            print("days = "+str(delta.days))
            if delta.days >= shutdownDays  and len(offServers) >=1:
                #print("Send mail")
                listOfInstOverTimeLimt.append({'tenant':tenant,'cloud':cloud,'id':instanceID,'instanceName':instanceName,'price':instancePrice,'ownerEmail':owner['email'],'servers':offServers})
        
    print("List of instances out of time = "+str(listOfInstOverTimeLimt))

    return listOfInstOverTimeLimt

def sendMail(instance,ownerEmail):
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    context = ssl._create_unverified_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, email_password)
        server.sendmail(sender_email, ownerEmail, instance)

def main():
    offlineInstances=getOfflineInstances()
    for i in offlineInstances:

        formattedMessage = formatInstanceForEmail(i)
        #print("print message" +formattedMessage)
        sendMail(formattedMessage,i['ownerEmail'])

main()

