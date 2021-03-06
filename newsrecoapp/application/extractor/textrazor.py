from application.config_import import get_private_config
from application.retrieval.data_retrieval import NewsRetrieval
import requests
import logging
import textrazor
import operator

class TextExtractor(object):
    """Wrapper for data retrieval functionality."""

    def __init__(self):
        """Empty, to be implemented by sub class."""
        pass

    def get_json_from_url(self, url):
        """Get the json response from a url, log if error."""
        response = requests.get(url)
        if response.status_code != 200:
            logging.error(
                "Response {} from server "
                "when accessing url {}".format(
                    response.status_code, url))
            return None
        return response.json(encoding='utf-8')

    def get_news_statistics(self, text):
        """Retrieve the list of topics(keywords) from the API for the given text."""
        textrazor.api_key = self.textrazor_apikey
        client = textrazor.TextRazor(extractors=["topics","entities"])
        client.set_classifiers(["textrazor_newscodes"])
        response = client.analyze(text)
        if len(response.topics())==0 and len(response.entities())==0 and len(response.categories())==0:
            return None
        return response

    # def get_news_topics(self, text):
    #     """Retrieve the list of topics(keywords) from the API for the given text."""
    #     textrazor.api_key = self.textrazor_apikey
    #     client = textrazor.TextRazor(extractors=["topics"])
    #     client.set_classifiers(["textrazor_newscodes"])
    #     response = client.analyze(text)
    #     return response.categories()
    #
    # def get_news_entities(self, text):
    #     """Retrieve the list of topics(keywords) from the API for the given text."""
    #     textrazor.api_key = self.textrazor_apikey
    #     client = textrazor.TextRazor(extractors=["topics"])
    #     client.set_classifiers(["textrazor_newscodes"])
    #     response = client.analyze(text)
    #     return response.categories()

class Extraction(TextExtractor):
    """Class Responsible to do analysis on news data."""

    def __init__(self):
        """Retrieve text razor api key."""
        super(TextExtractor, self).__init__()
        self.textrazor_apikey = get_private_config()["textrazorapi_key2"]

    def check_extraction_using_key(self):
        """
        Verify that the key is working by listing.

        the keywords information. It takes the second news from the news fetched
        from NewsApi and do extraction on News Description. Only topics with high
        relevance scores are listed. This should be stored in db.
        """
        news = NewsRetrieval()
        news_headline = news.get_news_headlines()
        print(news_headline['articles'][1]['description'])
        keywords = super().get_news_topics(news_headline['articles'][1]['description'])
        for keyword in sorted(keywords,key=operator.attrgetter('score'), reverse=True)[:5]:
                print(keyword.label)
        if keywords is None:
            return False
        return True