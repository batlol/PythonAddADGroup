# LDAP Integration with Python

This Python script integrates with an LDAP server to perform various operations such as searching for users and adding them to LDAP groups. The script utilizes the `ldap3` library for LDAP operations.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- `ldap3` library (`pip install ldap3`)
- `flask` library (`pip install flask`)
- `requests` library (`pip install requests`)

## Usage

1. Update the script with your LDAP server details and credentials:

    ```python
    # Define LDAP server details
    Server_ip = '192.168.2.3'

    # Define bind user credentials
    BIND_Username = 'TESTNETWERK\\Automation'
    BIND_Password = 'Welkom123!'
    ```

2. Modify the LDAP paths as per your LDAP configuration:

    ```python
    Base_DN = "dc=testnetwerk,dc=com"
    Group_DN = "CN=testgroup,CN=Users,DC=testnetwerk,DC=com"
    ```

3. Run the script. It will attempt to add the specified user to the LDAP group.

## Functions

### `server_ldap()`

- Creates an LDAP Server object.

### `connect_ldap()`

- Establishes a connection to the LDAP server.

### `find_user(username)`

- Searches for a user in the LDAP directory based on `sAMAccountName`.

### `add_user_to_group(username)`

- Adds the found user to the specified LDAP group.

## Error Handling

- The script includes error handling to catch exceptions that may occur during LDAP operations, such as connection errors or user not found.
