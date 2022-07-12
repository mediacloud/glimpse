import datetime as dt
from typing import List, Dict
import dateparser
import requests
import logging
from mediacloud.api import MediaCloud

from server.platforms.provider import ContentProvider
from server.util.cache import cache


class OnlineNewsMediaCloudProvider(ContentProvider):

    def __init__(self, api_key):
        super(OnlineNewsMediaCloudProvider, self).__init__()
        self._logger = logging.getLogger(__name__)
        self._api_key = api_key
        self._mc_client = MediaCloud(api_key)

    @cache.cache_on_arguments()
    def sample(self, query: str, start_date: dt.datetime, end_date: dt.datetime, limit: int = 20,
               **kwargs) -> List[Dict]:
        """
        Return a list of stories matching the query.
        :param query:
        :param start_date:
        :param end_date:
        :param limit:
        :param kwargs: sources and collections lists
        :return:
        """
        q, fq = self._format_query(query, start_date, end_date, **kwargs)
        story_list = self._mc_client.storyList(q, fq, rows=limit, **kwargs)
        return story_list

    @cache.cache_on_arguments()
    def count(self, query: str, start_date: dt.datetime, end_date: dt.datetime, **kwargs) -> int:
        """
        Count how many verified tweets match the query.
        :param query:
        :param start_date:
        :param end_date:
        :param kwargs: sources and collections lists
        :return:
        """
        q, fq = self._format_query(query, start_date, end_date, **kwargs)
        story_count_result = self._mc_client.storyCount(q, fq, **kwargs)
        return story_count_result['count']

    @cache.cache_on_arguments()
    def count_over_time(self, query: str, start_date: dt.datetime, end_date: dt.datetime, **kwargs) -> List[Dict]:
        """
        How many verified tweets over time match the query.
        :param query:
        :param start_date:
        :param end_date:
        :param kwargs: sources and collections lists
        :return:
        """
        q, fq = self._format_query(query, start_date, end_date, **kwargs)
        story_count_result = self._mc_client.storyCount(q, fq, split=True)
        return story_count_result

    #@cache.cache_on_arguments()
    def item(self, item_id: str) -> Dict:
        story = self._mc_client.story(item_id)
        return story

    @cache.cache_on_arguments()
    def words(self, query: str, start_date: dt.datetime, end_date: dt.datetime, limit: int = 100,
              **kwargs) -> List[Dict]:
        """
        Get the top words based on a sample
        :param query:
        :param start_date:
        :param end_date:
        :param limit:
        :param kwargs: sources and collections lists
        :return:
        """
        q, fq = self._format_query(query, start_date, end_date, **kwargs)
        top_words = self._mc_client.wordCount(q, fq, **kwargs)[:limit]
        return top_words

    @cache.cache_on_arguments()
    def tags(self, query: str, start_date: dt.datetime, end_date: dt.datetime, **kwargs) -> List[Dict]:
        q, fq = self._format_query(query, start_date, end_date, **kwargs)
        tags_sets_id = kwargs.get('tags_sets_id', None)
        sample_size = kwargs.get('sample_size', None)
        top_tags = self._mc_client.storyTagCount(q, fq, tag_sets_id=tags_sets_id, limit=sample_size, http_method='POST')
        return top_tags

    @classmethod
    def _format_query(cls, query: str, start_date: dt.datetime, end_date: dt.datetime,
                      **kwargs) -> (str, str):
        """
        Take all the query params and return q and fq suitable for a media cloud solr-syntax query
        :param query:
        :param start_date:
        :param end_date:
        :param kwargs: sources and collections
        :return:
        """
        media_ids = kwargs['sources'] if 'sources' in kwargs else []
        tags_ids = kwargs['collections'] if 'collections' in kwargs else []
        q = cls._query_from_parts(query, media_ids, tags_ids)
        fq = MediaCloud.dates_as_query_clause(start_date, end_date)
        return q, fq

    @classmethod
    def _query_from_parts(cls, query: str, media_ids: List[int], tag_ids: List[int]) -> str:
        query = '({})'.format(query)
        if len(media_ids) > 0 or (len(tag_ids) > 0):
            clauses = []
            # add in the media sources they specified
            if len(media_ids) > 0: # this format is a string of media_ids
                query_clause = "media_id:({})".format(" ".join([str(m) for m in media_ids]))
                clauses.append(query_clause)
            # add in the collections they specified
            if len(tag_ids) > 0: # this format is a string of tags_id_medias
                query_clause = "tags_id_media:({})".format(" ".join([str(m) for m in tag_ids]))
                clauses.append(query_clause)
            # now add in any addition media query clauses (get OR'd together)
            if len(clauses) > 0:
                query += " AND ({})".format(" OR ".join(clauses))
        return query


class OnlineNewsWaybackMachineProvider(ContentProvider):

    API_BASE_URL = "http://mcapi.sawood-dev.us.archive.org:8000/v1/"

    def __init__(self):
        super(OnlineNewsWaybackMachineProvider, self).__init__()
        self._logger = logging.getLogger(__name__)

    def sample(self, query: str, start_date: dt.datetime, end_date: dt.datetime, limit: int = 20,
               **kwargs) -> List[Dict]:
        results = self._overview_query(query, start_date, end_date, **kwargs)
        return self._matches_to_rows(results['matches'])

    def count(self, query: str, start_date: dt.datetime, end_date: dt.datetime, **kwargs) -> int:
        results = self._overview_query(query, start_date, end_date, **kwargs)
        return results['total']

    def count_over_time(self, query: str, start_date: dt.datetime, end_date: dt.datetime, **kwargs) -> Dict:
        results = self._overview_query(query, start_date, end_date, **kwargs)
        data = results['dailycounts']
        to_return = []
        for day_date, day_value in data.items():
            to_return.append({
                'date': dateparser.parse(day_date),
                'timestamp': dateparser.parse(day_date).timestamp(),
                'count': day_value,
            })
        return {'counts': to_return}

    @staticmethod
    def _date_query_clause(start_date: dt.datetime, end_date: dt.datetime) -> str:
        return "publication_date:[{} TO {}]".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    def _overview_query(self, query: str, start_date: dt.datetime, end_date: dt.datetime, **kwargs) -> Dict:
        params = {
            "q": "{} AND {}".format(query, self._date_query_clause(start_date, end_date))
        }
        results = self._query("search/overview", params)
        return results

    def item(self, item_id: str) -> Dict:
        results = self._query("article/{}".format(item_id))
        return results

    @cache.cache_on_arguments()
    def _query(self, endpoint: str, params: Dict = None) -> Dict:
        endpoint_url = self.API_BASE_URL+endpoint
        r = requests.get(endpoint_url, params=params)
        return r.json()

    @classmethod
    def _matches_to_rows(cls, matches: List) -> List:
        return [OnlineNewsWaybackMachineProvider._match_to_row(m) for m in matches]

    @classmethod
    def _match_to_row(cls, match: Dict) -> Dict:
        return {
            'media_name': match['canonical_domain'],
            'media_url': "http://"+match['canonical_domain'],
            'stories_id': match['article_url'].split("/")[-1],
            'title': match['article_title'],
            'publish_date': dateparser.parse(match['publication_date']),
            'url': match['original_url'],
            'language': match['language'],
        }
