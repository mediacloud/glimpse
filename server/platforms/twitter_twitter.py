import datetime as dt
import requests
import dateparser
from typing import List, Dict
import logging

from server.platforms.provider import ContentProvider, MC_DATE_FORMAT
from server.util.cache import cache

TWITTER_API_URL = 'https://api.twitter.com/2/'


class TwitterTwitterProvider(ContentProvider):

    def __init__(self, bearer_token=None):
        super(TwitterTwitterProvider, self).__init__()
        self._logger = logging.getLogger(__name__)
        self._bearer_token = bearer_token

    def sample(self, query: str, start_date: dt.datetime, end_date: dt.datetime, limit: int = 10, **kwargs) -> List[Dict]:
        """
        Return a list of historical tweets matching the query.
        :param query:
        :param start_date:
        :param end_date:
        :param limit:
        :param kwargs:
        :return:
        """
        # sample of historical tweets
        params = {
            "query": query,
            "max_results": limit,
            "start_time": start_date.isoformat("T") + "Z",
            "end_time": end_date.isoformat("T") + "Z",
            "tweet.fields": ",".join(["author_id", "created_at", "public_metrics"]),
            "expansions": "author_id"
        }
        results = self._cached_query("tweets/search/all", params)
        return TwitterTwitterProvider._tweets_to_rows(results)

    def count(self, query: str, start_date: dt.datetime, end_date: dt.datetime, **kwargs) -> int:
        over_time = self.count_over_time(query, start_date, end_date, **kwargs)
        total = sum([d['count'] for d in over_time['counts']])
        return total

    def count_over_time(self, query: str, start_date: dt.datetime,
                        end_date: dt.datetime, #ignored
                        **kwargs) -> Dict:
        """
        Count how many tweets match the query over the 31 days before end_date.
        :param query:
        :param start_date:
        :param end_date:
        :param kwargs:
        :return:
        """
        #  attenion over last 30 days
        params = dict(
            query=query,
            granularity='day',
            start_time=start_date.isoformat("T") + "Z",
            end_time=end_date.isoformat("T") + "Z",
        )
        results = self._cached_query("tweets/counts/all", params)
        data = []
        for d in results['data']:
            data.append({
                'date': dateparser.parse(d['start']),
                'timestamp': dateparser.parse(d['start']).timestamp(),
                'count': d['tweet_count'],
            })
        return {'counts': data}

    @cache.cache_on_arguments()
    def _cached_query(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Run a generic query agains the Twitter historical search API
        :param endpoint:
        :param query:
        :param params:
        :return:
        """
        headers = {
            'Content-type': 'application/json',
            'Authorization': "Bearer {}".format(self._bearer_token)
        }
        r = requests.get(TWITTER_API_URL+endpoint, headers=headers, params=params)
        return r.json()

    @classmethod
    def _add_author_to_tweets(cls, results: Dict) -> None:
        user_id_lookup = {u['id']: u for u in results['includes']['users']}
        for t in results['data']:
            t['author'] = user_id_lookup[t['author_id']]

    @classmethod
    def _tweets_to_rows(cls, results: Dict) -> List:
        TwitterTwitterProvider._add_author_to_tweets(results)
        return [TwitterTwitterProvider._tweet_to_row(t) for t in results['data']]

    @classmethod
    def _tweet_to_row(cls, item: Dict) -> Dict:
        link = 'https://twitter.com/{}/status/{}'.format(item['author']['username'], item['id'])
        return {
            'media_name': 'Twitter',
            'media_url': 'https://twitter.com/{}'.format(item['author']['username']),
            'stories_id': item['id'],
            'content': item['text'],
            'publish_date': dateparser.parse(item['created_at']),
            'url': link,
            'last_updated': dateparser.parse(item['created_at']),
            'author': item['author']['name'],
            'language': None,
            'retweet_count': item['public_metrics']['retweet_count'],
            'reply_count': item['public_metrics']['reply_count'],
            'like_count': item['public_metrics']['like_count'],
            'quote_count': item['public_metrics']['quote_count'],
        }
