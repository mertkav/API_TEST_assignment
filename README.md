# API Testing

### This repo contains API test automation to test https://gorest.co.in/ using the requests library of python

### test_config.yaml file includes the Bearer token which is need to authorization.

### test_api.py file includes the test documentation with scenarios.

### To run the tests type the command py.test test_api.py

1. Get all users.
2. Create a user
3. Create a userpost.
4. Create a comment on userpost.
5. Create a todo
6. Trying to create a new user with same e-mail
7. Create user without authorization
8. Create user without invalid e-mail adress.

### Prerequisites

Install prequisites using the below command

pip3 install -r requirements.txt


