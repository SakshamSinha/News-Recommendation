from __future__ import absolute_import, unicode_literals

import operator
import sys

sys.path.append("../")
from celery import shared_task
from datetime import datetime
from django.utils import timezone

from application.extractor.textrazor import Extraction
from application.models import NewsModel
from application.retrieval.data_retrieval import NewsRetrieval


@shared_task
def periodic_update_news():
    categories = []
    topics = []
    entities = []
    nrt= NewsRetrieval()
    extract = Extraction()
    news_dict = nrt.get_news_headlines()

    for news in news_dict['articles']:
        title = news['title'] if news['title'] is not None else " "
        description = news['description'] if news['description'] is not None else " "
        author = news['author']
        url = news['url']
        publishedAt = datetime.strptime(news['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        text = title + description
        if text== " ":
            continue
        else:
            response = extract.get_news_statistics(title+" "+description)
        if response == None:
            continue
        for category in sorted(response.categories(),key=operator.attrgetter('score'), reverse=True)[:5]:
            categories.append(category.label)
        for topic in sorted(response.topics(),key=operator.attrgetter('score'), reverse=True)[:5]:
            topics.append(topic.label)
        for entity in sorted(response.entities(),key=operator.attrgetter('relevance_score'), reverse=True)[:5]:
            entities.append(entity.id)
        keywords =topics + entities
        NewsModel.objects.create(
                title=title,
                description=description,
                author=author,
                url=url,
                published_at=publishedAt,
                keywords=keywords
        )
    print("Done adding the news")

