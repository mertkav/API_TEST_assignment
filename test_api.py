import requests
import pytest
import yaml
from requests.structures import CaseInsensitiveDict
import random


class TestUsers(object):

    format = "json"
    endpoint = "https://gorest.co.in"
    url = "/public/v2/users/"
    url_create_user_post = "/public/v2/users/4163/posts"
    url_comment = "/public/v2/posts/4163/comments"
    url_todo = "/public/v2/users/4163/todos"
    test_url = endpoint + url
    test_url_post = endpoint + url_create_user_post
    test_url_comment = endpoint + url_comment
    test_todo = endpoint + url_todo


    @staticmethod
    def search_key_in_response(full_response, search_for):
        """
        Test Helper method to find a specific string in the response body.
        """
        check = True
        user_list = full_response
        if search_for not in user_list.text:
            check = False
        else:
            user_list = user_list.json()
            for users in user_list:
                for keys in users:
                    if users[keys] == search_for:
                        check = True
        return check

    def setup_method(self):
        """
        Setup configrations is gathered by this method.
        """
        test_config_file = open("test_config.yaml", "r")
        setting = yaml.safe_load(test_config_file)
        self.headers = CaseInsensitiveDict()
        self.headers["Accept"] = setting["Content-Type"]
        self.headers["Authorization"] = setting["authorization"]

    @staticmethod
    def payload_generator():
        """
        This method returns payload Json
        """
        payload = {
            "name": "mert test10",
            "email": "mert" + "10" + "@mertmail.com",
            "gender": "male",
            "status": "active"
        }
        return payload



    def userpost_generator(self):

        userpost_data = {"title": "Create a post for testing",
                        "body": "This is the test body for the title"}
        return userpost_data

    def postcomment_generator(self):

        postcomment_data = {
                             "post_id": 1325,
                             "name": "mert test10",
                            "email": "mert" + "10" + "@mertmail.com",
                            "body": "Test post comment."
}
        return postcomment_data

        def todo_generator(self):
            todo_data = {
              "title": "todo testing.",
              "status": "completed"
}
            return todo_data

    @staticmethod
    def invalidpayload_generator():
        """
        This method returns payload with invalid e-mail
        """
        invalid_payload = {
            "name": "mert test10",
            "email": "mert" + "10" + "mertmail.com",
            "gender": "male",
            "status": "active"
        }
        return invalid_payload


    # Test-1

    def test_get_users(self):
        """
        To get user's information from https://gorest.co.in/public/v2/users
        """
        response = requests.get(self.test_url, headers=self.headers)
        assert response.status_code == 200

    # Test-2

    def test_create_a_user(self):
        """
        to create a user by name, email, gender, status
        """
        payload = self.payload_generator()
        response = requests.post(self.test_url, params=payload, headers=self.headers)
        assert response.status_code == 201
        # now checking if the user has been created or not using GET method.
        response_after = requests.get(self.test_url, params={"email": payload['email']}, headers=self.headers)
        assert self.search_key_in_response(response_after, payload['email'])

    # Test-3

    def test_create_a_userpost(self):
        """
        to create a userpost by title and body
        """
        userpost = self.userpost_generator()
        response = requests.post(self.test_url_post, params=userpost, headers=self.headers)
        assert response.status_code == 201
        # now checking if the user has been created or not using GET method.
        response_after = requests.get(self.test_url_post, params={"title": userpost['Create a post for testing']}, headers=self.headers)
        assert self.search_key_in_response(response_after, userpost['title'])

    # Test-4

    def test_create_a_postcomment(self):
        """
        to create a comment by title and body
        """
        postcomment = self.postcomment_generator()
        response = requests.post(self.test_url_comment, params=postcomment, headers=self.headers)
        assert response.status_code == 201
        # now checking if the user has been created or not using GET method.
        response_after = requests.get(self.test_url_comment, params={"body": postcomment['Test post comment.']}, headers=self.headers)
        assert self.search_key_in_response(response_after, postcomment['body'])

    # Test-5

    def test_create_a_todo(self):
        """
        to create a todo by title and status
        """
        todo = self.todo_generator()
        response = requests.post(self.url_todo, params=todo, headers=self.headers)
        assert response.status_code == 201
        # now checking if the user has been created or not using GET method.
        response_after = requests.get(self.url_todo, params={"title": todo['todo testing.']}, headers=self.headers)
        assert self.search_key_in_response(response_after, todo['title'])


    # Test-6

    def test_create_a_same_email_user(self):
        """
        try to create an existing user for the negative test scenario.
            1- creat a new user
            2- try to duplicate the same user again and return should be 422 status code.
        """

        ## 1
        payload = self.payload_generator()
        response = requests.post(self.endpoint + self.url, params=payload, headers=self.headers)
        assert response.status_code == 201

        ## 2
        response_duplicate = requests.post(self.endpoint + self.url, data=payload, headers=self.headers)
        assert response_duplicate.status_code == 422

    # Test-7

    def test_create_user_without_authentication(self):
        """
        try to create new user without authentication. status code should be 401
        """
        payload = self.payload_generator()
        response = requests.post(self.endpoint + self.url, params=payload)
        assert response.status_code == 401

    # Test-8

    def test_create_user_with_invalid_email(self):
        """
        try to create new user with invalid email. the response should be 404.
        """

        invalid_payload = self.invalidpayload_generator()
        response = requests.post(self.test_url, params=invalid_payload)
        assert response.status_code == 404


    # Test-9

    def test_update_user(self):
        """
        Eighth Case : user is successfully able to update user info with id
        """
        user_id = 23182
        update_test_url = self.test_url + str(user_id)
        payload = self.payload_generator()
        response = requests.patch(update_test_url, params=payload, headers=self.headers)
        assert response.status_code == 200
