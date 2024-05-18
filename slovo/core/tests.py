from django.test import TestCase, Client
from django.contrib.auth.models import User
from pprint import pprint
# Create your tests here.

class HomeTest(TestCase):
    c = Client(enforce_csrf_checks=False)

    def test_home(self):
        response = self.c.get("/")
        assert response.status_code == 200


class LoginTest(TestCase):
    # Create your tests here.
    c = Client(enforce_csrf_checks=False)

    def setUp(self) -> None:
        User.objects.create_user(username="john",email="password",password="johnnny_smith")

    def test_post_login(self):
        response = self.c.post("/login/", {"username": "john", "password": "johnny_smith"})
        assert response.status_code == 200 
    def test_get_login(self):
        response = self.c.get("/login/")
        assert response.status_code == 200 

class SignupTest(TestCase):

    c = Client()

    def test_signup_ok(self):

        response = self.c.post("/signup/",{"username":"user_test","email":"a@gmail.com","password1":"afiefffpozpapA4","password2":"afiefffpozpapA4"})
        usr = User.objects.get(username="user_test")
        User.objects.filter(username="user_test").exists() == True
        assert usr.username == 'user_test'
        assert response.status_code == 302 


    def test_signup_invalid(self):

        invalid_email = {"username":"azerty","email":"a@com","password1":"afiefffpozpapA4","password2":"afiefffpozpapA4"}
        invalid_pwd =  {"username":"azerty","email":"a@com","password1":"password","password2":"password"}
        not_same_pwd =  {"username":"azerty","email":"a@com","password1":"afiefffpozpapA","password2":"afiefffpozpapA4"}

        response_invalid_email = self.c.post("/signup/",invalid_email)
        assert User.objects.filter(username="azerty").exists() == False
        assert response_invalid_email.status_code == 200

        response_invalid_pwd = self.c.post("/signup/",invalid_pwd)
        assert User.objects.filter(username="azerty").exists() == False
        assert response_invalid_pwd.status_code == 200

        response_not_same_pwd = self.c.post("/signup/",not_same_pwd)
        assert User.objects.filter(username="azerty").exists() == False
        assert response_not_same_pwd.status_code == 200

        