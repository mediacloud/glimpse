import unittest
import datetime as dt

from server import TWITTER_API_BEARER_TOKEN
from server.platforms.twitter import TwitterTwitterProvider

TERM = "robots"


class TwitterTwitterProviderTest(unittest.TestCase):

    def setUp(self):
        self._provider = TwitterTwitterProvider(TWITTER_API_BEARER_TOKEN)

    def test_sample(self):
        results = self._provider.sample(TERM, start_date=dt.datetime.now() - dt.timedelta(days=5),
                                        end_date=dt.datetime.now())
        assert isinstance(results, list) is True
        for tweet in results:
            assert 'content' in tweet
            assert len(tweet['content']) > 0

    def test_samuel(self):
        q = '"racial healing" OR "race healing" OR "racial heal" OR "race heal"'
        start_date = dt.datetime(2020, 5, 2)
        end_date = dt.datetime(2022, 6, 30)
        total_tweets = self._provider.count(q, start_date=start_date, end_date=end_date)
        assert total_tweets > 0
        results = self._provider.count_over_time(q, start_date=start_date, end_date=end_date)
        assert total_tweets == results['total']

    def test_count(self):
        results = self._provider.count(TERM, start_date=dt.datetime.now() - dt.timedelta(days=5),
                                       end_date=dt.datetime.now())
        assert results > 0

    def test_count_over_time(self):
        results = self._provider.count_over_time(TERM, start_date=dt.datetime.now() - dt.timedelta(days=5),
                                                 end_date=dt.datetime.now())
        assert 'counts' in results
        assert isinstance(results['counts'], list) is True
        assert len(results['counts']) == 6
        total_check = sum([r['count'] for r in results['counts']])
        assert 'total' in results
        assert total_check == results['total']

    def test_longer_count_over_time(self):
        results = self._provider.count_over_time(TERM, start_date=dt.datetime.now() - dt.timedelta(days=45),
                                                 end_date=dt.datetime.now())
        assert 'counts' in results
        assert isinstance(results['counts'], list) is True
        assert len(results['counts']) == 46
