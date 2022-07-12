import unittest
import datetime as dt
import dateparser

from server.platforms.onlinenews import OnlineNewsMediaCloudProvider, OnlineNewsWaybackMachineProvider
from server import MEDIA_CLOUD_API_KEY


class OnlineNewsMediaCloudProviderTest(unittest.TestCase):

    def setUp(self):
        self._provider = OnlineNewsMediaCloudProvider(MEDIA_CLOUD_API_KEY)

    def test_count(self):
        results = self._provider.count("Trump", dt.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                        dt.datetime.strptime("2019-02-01", "%Y-%m-%d"))
        assert results > 0

    def test_sample(self):
        results = self._provider.sample("Trump", dt.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                        dt.datetime.strptime("2019-02-01", "%Y-%m-%d"))
        for post in results:
            assert 'url' in post

    def test_item(self):
        stories_id = 123123
        story = self._provider.item(stories_id)
        assert story['media_id'] == 15
        assert story['stories_id'] == stories_id
        assert len(story['title']) > 0

    def test_count_over_time(self):
        results = self._provider.count_over_time("Trump", dt.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                                 dt.datetime.strptime("2019-02-01", "%Y-%m-%d"))
        for item in results['counts']:
            assert 'date' in item
            assert 'count' in item

    def test_normalized_count_over_time(self):
        results = self._provider.normalized_count_over_time("Trump",
                                                            dt.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                                            dt.datetime.strptime("2019-02-01", "%Y-%m-%d"))
        assert 'counts' in results
        assert 'total' in results
        assert results['total'] > 0
        assert 'normalized_total' in results


class OnlineNewsWaybackMachineProviderTest(unittest.TestCase):

    def setUp(self):
        self._provider = OnlineNewsWaybackMachineProvider()

    def test_count(self):
        results = self._provider.count("coronavirus", dt.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                        dt.datetime.strptime("2019-02-01", "%Y-%m-%d"))
        assert results > 0

    def test_count_over_time(self):
        results = self._provider.count_over_time("coronavirus", dt.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                                 dt.datetime.strptime("2019-02-01", "%Y-%m-%d"))
        assert len(results) > 0
        for item in results['counts']:
            assert 'date' in item
            assert 'count' in item
            assert item['count'] > 0

    def test_sample(self):
        results = self._provider.sample("coronavirus", dt.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                        dt.datetime.strptime("2019-02-01", "%Y-%m-%d"))
        assert len(results) > 0
        for r in results:
            assert 'language' in r
            assert 'media_name' in r
            assert 'media_url' in r
            assert 'title' in r
            assert len(r['title']) > 0
            assert 'publish_date' in r
            assert r['publish_date'].year == 2019

    def test_item(self):
        STORY_ID = "Y29tLGV0dXJib25ld3Msc3EpLzU2Nzc5Mi90aGUtbGlnaHQtYXQtdGhlLWVuZC1vZi10aGUtY292aWQtMTktdHVubmVs"
        story = self._provider.item(STORY_ID)
        assert len(story['article_title']) > 0
        pub_date = dateparser.parse(story['publication_date'])
        assert pub_date.year == 2020
        assert pub_date.month == 3
        assert story['language'] == 'sq'
        assert story['canonical_domain'] == 'eturbonews.com'
        assert len(story['text_content']) > 0
