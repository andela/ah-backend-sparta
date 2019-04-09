from django.test import TestCase
from authors.apps.authentication.tests import (
    test_base, test_data
)
from authors.apps.articles.tests.test_data import (
    article_data, 
    test_user_data, 
    test_user2_data, 
    changed_article_data,
    article_data_no_body)
from rest_framework import status
from rest_framework.test import APITestCase

class TestArticle(test_base.BaseTestCase):

    def test_get_article_not_authenticated(self):
        user_token = self.create_user(test_data.test_user_data)
        resp =self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token, format='json')
        response = self.client.get('/api/articles/', format='json')
        title = response.data.get('results')[0].get('title')
        descr = response.data.get('results')[0].get('description')
        body = response.data.get('results')[0].get('body')
        self.assertEqual(title, article_data.get("title"))
        self.assertEqual(descr, article_data.get("description"))
        self.assertEqual(body, article_data.get("body"))

    def test_create_article(self):
        user_token = self.create_user(test_data.test_user_data)
        resp = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token, format='json')
        self.assertEqual(resp.data["article"]["title"], article_data.get("title"))
        self.assertEqual(resp.data["article"]["description"], article_data.get("description"))
        self.assertEqual(resp.data["article"]["body"], article_data.get("body"))
        self.assertEqual(resp.data["article"]['id'], int(1))
        self.assertEqual(resp.data["article"]["slug"], "hello-slug-first")
        self.assertEqual(resp.data["article"]["author"]["username"], "testuser")

    def test_get_article_authenticated(self):
        user_tkn = self.create_user(test_data.test_user_data)
        resp =self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_tkn, format='json')
        response = self.client.get('/api/articles/', HTTP_AUTHORIZATION=user_tkn, format='json')
        title = response.data.get('results')[0].get('title')
        body = response.data.get('results')[0].get('body')
        descr = response.data.get('results')[0].get('description')
        self.assertEqual(title, article_data.get("title"))
        self.assertEqual(descr, article_data.get("description"))
        self.assertEqual(body, article_data.get("body"))

    def test_get_article_by_id(self):
        user1_token = self.create_user(test_user_data)
        self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')

        all_articles = self.client.get('/api/articles/', HTTP_AUTHORIZATION=user1_token, format='json')
        id = all_articles.data.get('results')[0].get('id')

        response =self.client.get(f'/api/articles/{id}', HTTP_AUTHORIZATION=user1_token, format='json')

        self.assertEqual(response.data["title"], article_data["title"])
        self.assertEqual(response.data["description"], article_data.get("description"))
        self.assertEqual(response.data["body"], article_data.get("body"))

    def test_create_article_no_body(self):
        user_token = self.create_user(test_data.test_user_data)
        resp =self.client.post('/api/articles/', article_data_no_body, HTTP_AUTHORIZATION=user_token, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_owner_can_edit(self):
        user1_token = self.create_user(test_user_data)
        user2_token = self.create_user(test_user2_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        resp = self.client.put(f'/api/articles/{response.data["article"]["id"]}', article_data, HTTP_AUTHORIZATION=user2_token, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_str_model(self):
        user1_token = self.create_user(test_user_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        self.assertEqual(str(response.data["article"]["title"]), article_data["title"])
        