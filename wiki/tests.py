from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page
from django.utils.text import slugify

# Create your tests here.
class WikiPageTest(TestCase):

    def test_edit(self):
        user = User.objects.create_user(username='admin', password='djangopony')
        self.client.login(username='admin', password='djangopony')

        page = Page.objects.create(title="My Test Page", content="test", author=user)
        page.save()
        edit = {
            'title': 'testing title',
            'content': 'testing content'
        }

        response = self.client.post('/%s/' %slugify(page.title), edit)
        updated = Page.objects.get(title = edit['title'])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated.title, edit['title'])

    def test_page(self):
        user = User.objects.create_user(username='admin', password='djangopony')
        self.client.login(username='admin', password='djangopony')

        page = Page.objects.create(title="My Test Page", content="test", author=user)
        page.save()

        response = self.client.get('/%s/' %slugify(page.title))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')

    def test_create(self):
        user = User.objects.create_user(username='admin', password='djangopony')
        self.client.login(username='admin', password='djangopony')

        new = {
            'title': 'testing title',
            'content': 'testing content'
        }

        response = self.client.post('/wiki/new/', new)
        updated = Page.objects.get(title = new['title'])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated.title, new['title'])
'''
Steps to writing a test
    1. Set up your test data
    2. Make a request (GET, POST)
    3a. Check if response matches what we expect
    3b. Check if database matches what we expect
'''