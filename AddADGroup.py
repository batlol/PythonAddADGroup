# Import necessary modules and libraries
import requests
from flask import json
from ldap3 import Server, Connection, ALL_ATTRIBUTES, SUBTREE, NTLM
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups

# Test API data
testuser = r"TS\testuser"

# Define LDAP server details
Server_ip = '192.168.2.3'

# Define bind user credentials
BIND_Username = 'TESTNETWERK\\Automation'
BIND_Password = 'Welkom123!'

# Define LDAP paths
Base_DN = "dc=testnetwerk,dc=com"
Filter = "(sAMAccountName={0}*)"  # LDAP filter to search for users based on sAMAccountName
Group_DN = "CN=testgroup,CN=Users,DC=testnetwerk,DC=com"  # DN of the group to which users will be added

'''#
# #####################################################
# ######## untested topdesk API call###################
# #####################################################
#
# # TOPdesk API endpoint for searching incidents
# TOPDESK_API_URL = "https://TOPDESKURL.com/api/incidents"
#
# # TOPdesk API credentials
# TOPDESK_USERNAME = "test"
# TOPDESK_PASSWORD = "test123"
#
# def get_caller_name(incident):
#     # Extract callers name from the incident
#     caller = incident["caller"]["name"]
#     return caller
#
# def get_username():
#     # Define search parameters to find incidents with title starting with "AA21"
#     search_params = {
#         "query": "E2A*",
#         "limit": 1  # Limiting to 1 result as we only need one incident
#     }
#
#     try:
#         # Make a GET request to the TOPdesk API to search for incidents
#         response = requests.get(TOPDESK_API_URL, params=search_params, auth=(TOPDESK_USERNAME, TOPDESK_PASSWORD))
#         response.raise_for_status()  # Raise an exception for HTTP errors
#
#         # Parse the JSON response
#         data = response.json()
#
#         # Check if any incidents were found
#         if data["total"] > 0:
#             # Get the first incident found
#             incident = data["incidents"][0]
#
#             # Get reporter's network name from the incident
#             reporters_network_name = get_caller_name(incident)
#
#             print("Callers Name: ", reporters_network_name)
#         else:
#             print("No incidents found with title starting with 'AA21'")
#     except requests.exceptions.RequestException as e:
#         print("Error occurred:", e)
#
#
# #####################################################
# ######## end of untested topdesk API call############
# #####################################################
'''

# Function to create an LDAP Server object
def server_ldap():
    return Server(Server_ip)


# Function to establish connection to LDAP server
def connect_ldap():
    server = server_ldap()
    try:
        conn = Connection(server, user=BIND_Username, password=BIND_Password, authentication=NTLM, auto_bind=True)
        return conn
    except Exception as e:
        raise Exception("Failed to connect to LDAP server. Error: {}".format(str(e)))

# Function to search for a user in LDAP directory based on sAMAccountName
def find_user(username):
    with connect_ldap() as c:
        print("Connected to LDAP server")
        # Perform LDAP search operation
        c.search(search_base=Base_DN, search_filter=Filter.format(username[3:]), search_scope=SUBTREE,
                 attributes=ALL_ATTRIBUTES, get_operational_attributes=True)
        if not c.entries:
            raise Exception("User '{}' not found in LDAP directory.".format(username))
    # Return search results in JSON format
    return json.loads(c.response_to_json())


# Function to add the found user to the specified LDAP group
def add_user_to_group(username):
    try:
        # Retrieve the DN (Distinguished Name) of the user from search results
        user = find_user(username)["entries"][0]["dn"]
        # Add user to the specified group
        ad_add_members_to_groups(connect_ldap(), user, Group_DN)
        return "Added " + user + " to the group!"
    except Exception as e:
        raise Exception("Failed to add user to group. Error: {}".format(str(e)))


# Add user to the group
try:
    # Attempt to add test user to the group and print confirmation
    print(add_user_to_group(testuser))
except Exception as e:
    # Print error message if an exception occurs
    print("Error:",e)

