import boto3
import sys
from morpheuscypher import Cypher
from botocore.config import Config


def ec2_client(region_name,access_key,access_secret,proxy_definitions):
    """
    Connects to EC2, returns a connection object
    """
    
    try:
        if proxy_definitions:
            conn = boto3.client('ec2',region_name=region_name,aws_access_key_id=access_key,aws_secret_access_key=access_secret,config=Config(proxies=proxy_definitions))
        else:
            conn = boto3.client('ec2',region_name=region_name,aws_access_key_id=access_key,aws_secret_access_key=access_secret)
 
    except Exception as e:
        sys.stderr.write(
            'Could not connect to region: %s. Exception: %s\n' % (region, e))
        conn = None
 
    return conn


#No proxy
proxy_definitions = {}

#With proxy creds
#proxy_definitions = {
#    'https': 'username:password@proxy_address:3128'
#}

#Without proxy creds
#proxy_definitions = {
#    'https': 'proxy_address:3128'
#}

#AWS creds loaded from Morpheus Cypher
c = Cypher(morpheus=morpheus,ssl_verify=False)
access_key=c.get("secret/aws_access_key")
access_secret=c.get("secret/aws_access_secret")

default_region="eu-west-2"

client = ec2_client(default_region,access_key,access_secret,proxy_definitions)

vpcs = client.describe_vpcs()

for v in vpcs['Vpcs']:
    print("vpc id= ",v['VpcId'])
