from xmlrpc import client
import os

server_url = 'http://localhost:1769'
db_name = 'v17e_test'


# Create login in terminal with: export TEST_USERNAME=""
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")
common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)

version_info = common.version()
print(version_info)

user_id = common.authenticate(db_name, username, password, {})
if user_id:
    print("Success: User id is", user_id)
else:
    print("Failed: wrong credentials")