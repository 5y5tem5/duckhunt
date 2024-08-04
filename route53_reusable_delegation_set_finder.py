import boto3
import datetime
import random
import string
import sys
import time
today_date = datetime.datetime.now().strftime('%Y-%m-%d')
random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
caller_reference_base = today_date +"-"+random_chars+"-"
def create_reusable_delegation_set(client, caller_reference):
    return client.create_reusable_delegation_set(
        CallerReference=caller_reference
    )

def delete_reusable_delegation_set(client, delegation_set_id):
    client.delete_reusable_delegation_set(
        Id=delegation_set_id
    )

def main():
    # Initialize a Route 53 client
    client = boto3.client('route53')

    # Sets vars
    dnsserver =""
    counter =0
    needed_server="ns-1017.awsdns-63.net"
    #main loop
    while(dnsserver !=needed_server):
        #safety measure
        time.sleep(1)
        counter+=1
        print(f"counter is {counter}")
        caller_reference = caller_reference_base+str(counter)
        print(f"caller_reference is {caller_reference}")
        response = create_reusable_delegation_set(client, caller_reference)
        name_servers = response['DelegationSet']['NameServers']
        print(f"name_servers is {name_servers}")
        delegation_set_id = response['DelegationSet']['Id']
        # Check if any of the name servers matches our needed name server
        for name_server in name_servers:
            if name_server.endswith(needed_server):
                dnsserver = name_server
                print(f"delegation_set_id: {delegation_set_id}")
                sys.exit(0)
        #we got here so dns server is not in our list as such lets delete this reusable_delegation_set
        print(f"deleting {delegation_set_id}")
        delete_reusable_delegation_set(client, delegation_set_id)

if __name__ == "__main__":
    main()
