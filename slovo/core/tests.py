from django.test import TestCase, Client
from django.contrib.auth.models import User
from pprint import pprint
from core.views import credentials_taken
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
        User.objects.all().delete()
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

class UserSettingsTest(TestCase):

    url = "/settings/"
    c = Client()
    anonymous_client = Client()
    def setUp(self)->None:
        User.objects.all().delete()
        self.user = User.objects.create_user(username="footer",email="foot@toe.com",password="weird_fetish")
        self.c.login(username="footer", password="weird_fetish")

    def test_settings_status(self):
        
        response = self.c.get(self.url)
        assert response.status_code == 200 

        response = self.anonymous_client.get(self.url)
        assert response.status_code == 302 # redirection
    
    def test_username_change(self):
        username = "header"
        response = self.c.post(self.url,{"email_username":['Składać'],"username":username,"email":"foot@toe.com"})
        assert response.status_code == 302
        assert User.objects.filter(username=username,email="foot@toe.com").exists()
    
    def test_password_change(self):
        # 1. Password change
        former_pwd , new_pwd , confirm_pwd = "weird_fetish", "all_tastes_are_equals", "all_tastes_are_equals"
        response = self.c.post(self.url,{"password":['Składać'],"former_pwd":former_pwd,"new_pwd":new_pwd,"confirm_pwd":confirm_pwd})    
        assert response.status_code == 302 

        # 2. Confirmation and new password do not match 
        new_pwd2 , confirm_pwd =  "all_tastes_are_equals", "or_maybe_not_so_much"
        User.objects.create_user(username="test2",email="footixxx@toe.com",password=new_pwd2)
        self.c.login(username="test2", password=new_pwd2)
        response = self.c.post(self.url,{"password":['Składać'],"former_pwd":new_pwd,"new_pwd":new_pwd2,"confirm_pwd":confirm_pwd})    
        assert response.status_code ==  200
    def test_email_change(self):
        email  ="header@toe.com"
        response = self.c.post(self.url,{"email_username":['Składać'],"username":"footer","email":email})
        assert response.status_code == 302
        assert User.objects.filter(username="footer",email=email).exists()
            
    def test_delete_account(self):
        response = self.c.post("/delete/")
        assert response.status_code == 302
        assert User.objects.filter(username="footer",email="header@toe.com").exists() == False
        
class FooterTest(TestCase):

    c = Client()
    anonymous_client = Client()

    def setUp(self)->None:
        User.objects.all().delete()
        user = User.objects.create_user(username="footer",email="foot@toe.com",password="weird_fetish")
        self.c.login(username="footer", password="weird_fetish")
        
    def test_terms_of_use(self):
        response = self.anonymous_client.get("/terms_of_use/")
        assert response.status_code == 200 
    
    def test_about(self):
        response = self.anonymous_client.get("/about/")
        assert response.status_code == 200 

    def test_privacy(self):
        response = self.anonymous_client.get("/privacy/")
        assert response.status_code == 200 

    def test_contact(self):
        response = self.anonymous_client.get("/contact/")
        assert response.status_code == 200 
