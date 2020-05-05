import unittest

from django.test import TestCase, Client
from django.contrib.auth.models import User
from wiki.models import Page

# Create your tests here.
class WikiTestCase(TestCase):
    def test_true_is_tru(self):
        """Tests if True == True. Should always work"""
        self.assertEqual(True, True)

    def test_page_slugify_on_save(self):
        """Tests slug generated when saving Page."""
        # Author is a required field in our model
        # Create a user for this test and save it to the test database
        user = User()
        user.save()

        # Create and save a new page to the test database
        page = Page(title="My Test Page", content = "test", author = user)
        page.save()
        response = self.client.get('')

        # Make sure the slug that was generated in Page.save()
        # Matches to what we think it should be
        self.assertEqual(page.slug, "my-test-page")
        self.assertEqual(response.status_code, 200)

class PageListViewTests(TestCase):
    def test_multiple_pages(self):
        # Make some test data to be displayed on the page
        user = User.objects.create()

        Page.objects.create(title="My Test Page", content="test", author=user)
        Page.objects.create(title="Another Test Page", content="test", author=user)

        # Issue a GET request to the MakeWiki homepage.
        # When we make a request, we get a response back.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the number of pages passed to the template
        # matches the number of pages we have in the database.
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

        self.assertQuerysetEqual(
            responses,
            ['<Page: My Test Page>', '<Page: Another Test Page>'],
            ordered=False
        )


class PageDetailViewTests(TestCase):
    # Set up the data
    def test_detail_page(self):
        user = User.objects.create()
        data = {'title': "My test page.",
                'author': user,
                'content' : "test form"}
        response = self.client.post('/submit/', data)
        self.assertEqual(response.status_code, 302)

class PageCreateViewTests(TestCase):
    def test_create_page(self):
        user = User.objects.create()
        data = {'title': "A test page",
            'author': user,
            'content': "Another test"}
        response = self.client.post('/submit/', data)
        self.assertEqueal(response.status_code, 302) 
'''
Steps to writing a test
    1. Set up your test data
    2. Make a request (GET, POST)
    3a. Check if response matches what we expect
    3b. Check if database matches what we expect
'''