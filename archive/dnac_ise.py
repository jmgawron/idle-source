import getpass
import requests
import base64
import datetime
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#### Static stuff
HEADERS = {'Content-type': 'application/json'}
SEPARATOR = "============================================="


#### DNA Prompts and defaults
api_base_path = "https://10.201.37.80/api"
b64cred = ""
dna_token = ""
dna_token_expires = datetime.datetime.now()


def main():
    get_credentials()
    get_service_token()

    json_ise_integration = get_ise_integration()

    if len(json_ise_integration["response"]) == 0:
        print("no response on ise integration, run ise setup?")
    else:
        print_ise_integration(json_ise_integration)

    #if datetime.datetime.now() > dna_token_expires:
    #    get_service_token()

    #get_groupings()


def get_credentials():
    global dna_username, dna_password, b64cred
    print(SEPARATOR)
    print("Connecting to: " + api_base_path)
    print(SEPARATOR)
    dna_username = input("DNA ADMIN USERNAME: ")
    dna_password = getpass.getpass("DNA ADMIN PASSWORD: ")
    creds = dna_username + ':' + dna_password
    b64cred = base64.b64encode(creds.encode('utf8'))


def get_service_token():
    global dna_token, dna_token_expires
    print("")
    print(SEPARATOR)
    print("Updating DNA API Service Token")
    print(SEPARATOR)
    # Request a new service token
    body = { "username": dna_username,
        "password": dna_password
        }
    hyperURL = api_base_path + "/system/v1/auth/token"
    response = requests.post(hyperURL, data=json.dumps(body), verify=False,
                             headers={'Authorization': 'Basic {}'.format(b64cred.decode('utf8'))})
    print("Return Code: " + str(response.status_code))
    if response.status_code != 200:
        print("Login failed.  Please re-enter credentials:")
        get_credentials()
        get_service_token()
        return
    json_service_token = json.loads(response.content)
    dna_token = json_service_token["Token"]
    print("DNA Token: " + dna_token)
    #dna_token_expires = datetime.datetime.now() + datetime.timedelta(seconds=json_service_token["response"]["idleTimeout"])
    #print("DNA Token Expires: " + dna_token_expires.ctime())


## Ok, assummes ISE is up ##
def get_ise_integration():
    print(SEPARATOR)
    print("Get ISE Integration Configuration")
    print(SEPARATOR)
    header = {'Content-type': 'application/json', "X-Auth-Token": dna_token}
    hyperURL = api_base_path + "/v1/aaa/"
    response = requests.get(hyperURL, verify=False, headers=header)
    #print(response)
    print("Return Code: " + str(response.status_code))
    #print(json.loads(response.content))
    return json.loads(response.content)


def print_ise_integration(data):
    print(SEPARATOR)
    print(" ISE Integration status: ")
    print("    Role.................." + str(data["response"][0]["role"]))
    print("    IP Address............" + str(data["response"][0]["ipAddress"]))
    print("    Authentication Port..." + str(data["response"][0]["authenticationPort"]))
    print("    Accounting Port......." + str(data["response"][0]["accountingPort"]))
    print("    Enabled..............." + str(data["response"][0]["isIseEnabled"]))
    print("    State................." + str(data["response"][0]["state"]))
    print("    Trust State..........." + str(data["response"][0]["ciscoIseDtos"][0]["trustState"]))
    print("    Failure Reason........" + str(data["response"][0]["ciscoIseDtos"][0]["failureReason"]))


## Need to define get_groups() ##
def get_groupings():
    print("")
    print(SEPARATOR)
    print("Get Area/Building/Floor Groupings")
    print(SEPARATOR)
    #return get_groups()


if __name__ == "__main__":
    main()
