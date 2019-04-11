from django.urls import reverse
from authors.apps.comments.models import Comment
from authors.apps.authentication.tests.test_base import BaseTestCase
from rest_framework import status
from .test_data import (
    register_user1_data,
    update_user_profile_data1,
    article_data,
    comment_data,
    comment_data1,
    reply_to_comment1,
    reply_to_comment2,
    update_comment_data,
    register_user2_data
)


class TestArticleComments(BaseTestCase):
    """
    Class to handle tests of article comments
    """

    def test_adding_comment_to_an_article(self):
        """
        Method to test creating a comment on an article
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token1,
                                     format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        self.assertEqual(response3.data["body"], "We love our TTl")
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

    def test_replying_to_comment(self):
        """
        Method to test replying to a comment
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}),
                                     comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1, format='json')
        response5 = self.client.post(reverse('articles:create-article-comment-reply',
                                             kwargs={'slug': response2.data["article"]["slug"],
                                                     'pk': response4.data[0]["id"]},
                                             ), reply_to_comment1,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )

        self.assertEqual(response5.data["body"], "He replies to slack texts instantly")
        self.assertEqual(response5.status_code, status.HTTP_200_OK)

    def test_getting_all_comments(self):
        """
        Method to test getting all comments
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data,
                                     HTTP_AUTHORIZATION=user_token1, format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        response4 = self.client.get('/api/comments',
                                    HTTP_AUTHORIZATION=user_token1, format='json')
        self.assertEqual(response4.data[0]["body"], "We love our TTl")
        self.assertEqual(response4.status_code, status.HTTP_200_OK)

    def test_getting_a_single_comment(self):
        """
        Method to test getting a single comment
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data,
                                     HTTP_AUTHORIZATION=user_token1, format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response5 = self.client.get(reverse(
            'comments:comment-detail',
            kwargs={'pk': response4.data[0]["id"]}

        ), HTTP_AUTHORIZATION=user_token1, format='json')
        self.assertEqual(response4.data[0]["body"], "We love our TTl")
        self.assertEqual(response4.status_code, status.HTTP_200_OK)

    def test_get_replies_to_a_comment(self):
        """
        Method to test getting replies for a given comment
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token1,
                                     format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}),
                                     comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1, format='json')
        self.client.post(reverse('articles:create-article-comment-reply',
                                 kwargs={'slug': response2.data["article"]["slug"],
                                         'pk': response4.data[0]["id"]},
                                 ), reply_to_comment1,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        self.client.post(reverse('articles:create-article-comment-reply',
                                 kwargs={'slug': response2.data["article"]["slug"],
                                         'pk': response4.data[0]["id"]},
                                 ), reply_to_comment2,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        response5 = self.client.get(reverse(
            'comments:comment-replies',
            kwargs={'parent_id': response4.data[0]["id"]}

        ), HTTP_AUTHORIZATION=user_token1, format='json')
        self.assertEqual(response5.data[0]["body"], "He replies to slack texts instantly")
        self.assertEqual(response5.data[1]["body"], "He makes coding fun")
        self.assertEqual(response4.status_code, status.HTTP_200_OK)

    def test_retrieve_article_comment_details(self):
        """
        Method to test getting comment details of an article
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data,
                                     HTTP_AUTHORIZATION=user_token1, format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1, format='json')
        self.client.post(reverse('articles:create-article-comment-reply',
                                 kwargs={'slug': response2.data["article"]["slug"],
                                         'pk': response4.data[0]["id"]},
                                 ), reply_to_comment1,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        self.client.post(reverse('articles:create-article-comment-reply',
                                 kwargs={'slug': response2.data["article"]["slug"],
                                         'pk': response4.data[0]["id"]},
                                 ), reply_to_comment2,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        response5 = self.client.get(reverse(
            'articles:articles-comments-details',
            kwargs={'slug': response2.data["article"]["slug"]}

        ), HTTP_AUTHORIZATION=user_token1, format='json')
        self.assertEqual(response5.data["comments"][0]["reply_count"], 2)
        self.assertEqual(response5.status_code, status.HTTP_200_OK)

    def test_updating_an_article_comment(self):
        """
        Method to test updating an article comment
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token1,
                                     format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}),
                                     comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1, format='json')
        response5 = self.client.put(reverse('articles:delete-update-comment',
                                            kwargs={'slug': response2.data["article"]["slug"],
                                                    'pk': response4.data[0]["id"]},
                                            ), update_comment_data,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json'
                                    )
        self.assertEqual(response5.data["body"], "Updated by Francis")
        self.assertEqual(response5.status_code, status.HTTP_200_OK)

    def test_updating_an_article_comment_that_your_not_owner(self):
        """
        Method to test updating an article comment
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token1,
                                     format='json')
        response3 = self.client.post(reverse('articles:create-article-comment',
                                             kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                                     HTTP_AUTHORIZATION=user_token1,
                                     format='json'
                                     )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1, format='json')
        response5 = self.client.put(reverse('articles:delete-update-comment',
                                            kwargs={'slug': response2.data["article"]["slug"],
                                                    'pk': response4.data[0]["id"]},
                                            ), update_comment_data,
                                    HTTP_AUTHORIZATION=user_token2,
                                    format='json'
                                    )
        self.assertEqual(response5.data["message"], "You can only update your comment")
        self.assertEqual(response5.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_a_comment(self):
        """
        Method to test deleting a comment
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token1,
                                     format='json')
        self.client.post(reverse('articles:create-article-comment',
                                 kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        self.client.post(reverse('articles:create-article-comment',
                                 kwargs={'slug': response2.data["article"]["slug"]}), comment_data1,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        self.client.post(reverse('articles:create-article-comment',
                                 kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1, format='json')

        response5 = self.client.delete(reverse(
            'articles:delete-update-comment',
            kwargs={'slug': response2.data["article"]["slug"], 'pk': response4.data[0]["id"]}

        ), HTTP_AUTHORIZATION=user_token1)
        self.assertEqual(response5.data["message"], "Comment has been successfully deleted")
        self.assertEqual(response5.status_code, status.HTTP_200_OK)

    def test_deleting_a_comment_that_user_does_not_own(self):
        """
        Method to test deleting a comment that doesnt belog to the commentor
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1,
                                    HTTP_AUTHORIZATION=user_token1,
                                    format='json')
        response2 = self.client.post('/api/articles/', article_data, HTTP_AUTHORIZATION=user_token1,
                                     format='json')
        self.client.post(reverse('articles:create-article-comment',
                                 kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        self.client.post(reverse('articles:create-article-comment',
                                 kwargs={'slug': response2.data["article"]["slug"]}), comment_data1,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        self.client.post(reverse('articles:create-article-comment',
                                 kwargs={'slug': response2.data["article"]["slug"]}), comment_data,
                         HTTP_AUTHORIZATION=user_token1,
                         format='json'
                         )
        response4 = self.client.get('/api/comments', HTTP_AUTHORIZATION=user_token1, format='json')

        response5 = self.client.delete(reverse(
            'articles:delete-update-comment',
            kwargs={'slug': response2.data["article"]["slug"], 'pk': response4.data[0]["id"]}

        ), HTTP_AUTHORIZATION=user_token2)
        self.assertEqual(response5.data["message"], "You can only delete your comment")
        self.assertEqual(response5.status_code, status.HTTP_403_FORBIDDEN)
