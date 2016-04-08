#-*- coding: UTF-8 -*-
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.core.management import call_command

from movimento.views import index


class DashboardTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'fixtures/json/configuracoes_parametrizacao/fixture.json', verbosity=0)
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user_teste', email='user_teste@email.com.br', password='**...**')


    def test_access_user_anonymous(self):
        # Create an instance of a GET request.
        request = self.factory.get('/dashboard/')
        
        # Simulate an anonymous user by setting request.user to an AnonymousUser instance.
        request.user = AnonymousUser()
        
        # Test index() as if it were deployed at /dashboard/
        response = index(request)

        self.assertEqual(response.status_code, 302)


    def test_access_user_authenticated(self):
        # Create an instance of a GET request.
        request = self.factory.get('/dashboard/')
        
        # Recall that middleware are not supported. You can simulate a logged-in user by setting request.user manually.
        request.user = self.user
        
        # Test index() as if it were deployed at /dashboard/
        response = index(request)

        self.assertEqual(response.status_code, 200)