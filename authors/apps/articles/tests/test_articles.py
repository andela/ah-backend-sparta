from unittest import mock

from rest_framework import status
from authors.apps.articles.models import  Article

from authors.apps.articles.models import Article
from authors.apps.authentication.tests import (
    test_base, test_data
)
from authors.apps.articles.tests.test_data import (
    article_data, 
    test_user_data, 
    test_user2_data, 
    changed_article_data,
    article_data_no_body,
    like_data, dislike_data
    )
from rest_framework import status
from rest_framework.test import APITestCase
from authors.apps.articles.models import Article

class TestArticle(test_base.BaseTestCase):

    def test_get_article_not_authenticated(self):
        user_token = self.create_user(test_data.test_user_data)
        resp = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token, format='json')
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
        self.assertEqual(resp.data["article"]["slug"], "hello-slug-first")
        self.assertEqual(resp.data["article"]["author"]["username"], "testuser")

    def test_get_article_authenticated(self):
        user_tkn = self.create_user(test_data.test_user_data)
        resp = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_tkn, format='json')
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
        slug = all_articles.data.get('results')[0].get('slug')

        response = self.client.get(f'/api/articles/{slug}', HTTP_AUTHORIZATION=user1_token, format='json')

        self.assertEqual(response.data["title"], article_data["title"])
        self.assertEqual(response.data["description"], article_data.get("description"))
        self.assertEqual(response.data["body"], article_data.get("body"))

    def test_create_article_no_body(self):
        user_token = self.create_user(test_data.test_user_data)
        resp = self.client.post('/api/articles/', article_data_no_body, HTTP_AUTHORIZATION=user_token, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_owner_can_edit(self):
        user1_token = self.create_user(test_user_data)
        user2_token = self.create_user(test_user2_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        resp = self.client.put(f'/api/articles/{response.data["article"]["slug"]}', article_data, HTTP_AUTHORIZATION=user2_token, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_str_model(self):
        mock_instance = mock.Mock(spec=Article)
        mock_instance.title = "hello slug"
        mock_instance.description = "Short description about slug"
        self.assertEqual(Article.__str__(mock_instance), "hello slug")
        
    def test_like_an_article(self):
        user1_token = self.create_user(test_user_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        liked_article_id = response.data["article"]["slug"]
        user1_like_resp = self.client.post(f'/api/articles/{liked_article_id}/like', like_data,
                                            HTTP_AUTHORIZATION=user1_token, format='json')
        self.assertEqual(like_data["likes"], user1_like_resp.data["details"]["likes"])
        user1_like_again = self.client.post(f'/api/articles/{liked_article_id}/like', like_data,
                                            HTTP_AUTHORIZATION=user1_token, format='json')
        self.assertEqual({'msg': 'You have already liked this article'}, user1_like_again.data)  

    def test_dislike_an_article(self):
        user1_token = self.create_user(test_user_data) 
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        user1_dislike_resp = self.client.post(f'/api/articles/{response.data["article"]["slug"]}/like', dislike_data,
                                            HTTP_AUTHORIZATION=user1_token, format='json') 
        self.assertEqual(dislike_data["likes"], user1_dislike_resp.data["details"]["likes"])
        user1_dislike_again = self.client.post(f'/api/articles/{response.data["article"]["slug"]}/like', dislike_data,
                                            HTTP_AUTHORIZATION=user1_token, format='json')   
        self.assertEqual({'msg': 'You have already disliked this article'}, user1_dislike_again.data)    

    def test_another_user_can_like(self):
        user1_token = self.create_user(test_user_data)
        user2_token = self.create_user(test_user2_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        user1_like_resp = self.client.post(f'/api/articles/{response.data["article"]["slug"]}/like', like_data,
                                            HTTP_AUTHORIZATION=user1_token, format='json')
        user2_like_resp = self.client.post(f'/api/articles/{response.data["article"]["slug"]}/like', like_data,
                                            HTTP_AUTHORIZATION=user2_token, format='json')
        get_articles = self.client.get('/api/articles/')
        self.assertEqual(2, get_articles.data["results"][0]["likes"])

    def test_like_then_dislike(self):
        user1_token = self.create_user(test_user_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user1_token, format='json')
        user1_like_resp = self.client.post(f'/api/articles/{response.data["article"]["slug"]}/like', like_data,
                                            HTTP_AUTHORIZATION=user1_token, format='json')
        user1_dislike_resp = self.client.post(f'/api/articles/{response.data["article"]["slug"]}/like', dislike_data,
                                            HTTP_AUTHORIZATION=user1_token, format='json')
        self.assertEqual(dislike_data["likes"], user1_dislike_resp.data["details"]["likes"]) 

    def test_favorite_article(self):
        user_token = self.create_user(test_data.test_user_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token, format='json')
        article_slug = response.data['article']['slug']
        response1 = self.client.post(f'/api/articles/{article_slug}/favorite', {'favorite': True}, HTTP_AUTHORIZATION=user_token, format='json')
        response2 = self.client.post(f'/api/articles/{article_slug}/favorite', {'favorite': True}, HTTP_AUTHORIZATION=user_token, format='json')
        response3 = self.client.post(f'/api/articles/{article_slug}/favorite', {'favorite': False}, HTTP_AUTHORIZATION=user_token, format='json')
        response4 = self.client.post(f'/api/articles/{article_slug}/favorite', {'favorite': False}, HTTP_AUTHORIZATION=user_token, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_list(self):
        user_token = self.create_user(test_data.test_user_data)
        response = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token, format='json')
        article_slug = response.data['article']['slug']
        response1 = self.client.post(f'/api/articles/{article_slug}/favorite', None, HTTP_AUTHORIZATION=user_token, format='json')
        response2 = self.client.get(f'/api/users/articles/favorites', HTTP_AUTHORIZATION=user_token, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


    def test_article_contains_share_links(self):
        """
        Test article contains share links
        """
        user_token = self.create_user(test_data.test_user_data)
        resp = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token, format='json')
        response = self.client.get('/api/articles/', format='json')
        self.assertEqual(response.data["results"][0]["share_article_links"]["facebook"], 
        'https://www.facebook.com/sharer/sharer.php?u=http%3A//testserver/api/articles/hello-slug-first')
        self.assertEqual(response.data["results"][0]["share_article_links"]["twitter"], 
        'https://twitter.com/home?status=http%3A//testserver/api/articles/hello-slug-first')
        self.assertEqual(response.data["results"][0]["share_article_links"]["googleplus"], 
        'https://plus.google.com/share?url=http%3A//testserver/api/articles/hello-slug-first')
        self.assertEqual(response.data["results"][0]["share_article_links"]["email"], 
        'mailto:?&subject=hello%20slug&body=hello%20slug%0A%0Ahttp%3A//testserver/api/articles/hello-slug-first')
