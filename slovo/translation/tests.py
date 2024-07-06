from django.test import TestCase , Client
from django.contrib.auth.models import User

class TranslationTest(TestCase):

    c = Client(enforce_csrf_checks=False)
    a_c = Client(enforce_csrf_checks=False)
    
    url = "/translate/"
    def setUp(self) -> None:
        User.objects.all().delete()
        user = User.objects.create_user(username="translate_user",email="transl@toe.com",password="whynot12345678")
        self.c.login(username="translate_user",password="whynot12345678")
    
    def test_unauthenticated(self):
        """
        Unauthenticated requests should be redirection
        """
        response = self.a_c.get(self.url)
        assert response.status_code == 302

        response = self.a_c.post(self.url)
        assert response.status_code == 302

    def test_authenticated(self):

        response = self.c.get(self.url)
        assert response.status_code == 200