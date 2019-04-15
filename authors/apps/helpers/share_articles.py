import urllib.parse
from django.urls import reverse
from django.conf import settings

def share_articles_links(obj, request):
    """
    Generates sharing links for popular plaforms
    like facebook, googleplus, twitter and email

    Args:
        article_title(String): title of article to share
        article_link(String): http link to article

    returns
        share_links(dict): collection of sharing links

    """
    share_links = {}
    article_title = obj.title
    article_link = f'{settings.BASE_ARTICLE_SHARE_URL}/{obj.slug}' if settings.BASE_ARTICLE_SHARE_URL else \
        request \
            .build_absolute_uri(reverse('articles:auth-articles', \
                                        kwargs={'slug': obj.slug}))

    encoded_article_link = urllib.parse.quote(article_link)
    encoded_article_title = urllib.parse.quote(article_title)

    share_links['facebook'] = 'https://www.facebook.com/sharer/sharer.php?u=' + encoded_article_link
    share_links['twitter'] = 'https://twitter.com/home?status=' + encoded_article_link
    share_links['googleplus'] = 'https://plus.google.com/share?url=' + encoded_article_link
    share_links['email'] = 'mailto:?&subject=' + encoded_article_title + '&body=' \
                           + encoded_article_title + '%0A%0A' + encoded_article_link
    return share_links
