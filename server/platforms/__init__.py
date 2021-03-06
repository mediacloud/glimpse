import logging
from typing import List

from server import YOUTUBE_API_KEY, TWITTER_API_BEARER_TOKEN, MEDIA_CLOUD_API_KEY
from server.platforms.provider import ContentProvider
from server.platforms.reddit import RedditPushshiftProvider
from server.platforms.twitter import TwitterTwitterProvider
from server.platforms.youtube import YouTubeYouTubeProvider
from server.platforms.onlinenews import OnlineNewsMediaCloudProvider

logger = logging.getLogger(__name__)

# static list matching topics/info results
PLATFORM_TWITTER = 'twitter'
PLATFORM_REDDIT = 'reddit'
PLATFORM_YOUTUBE = 'youtube'
PLATFORM_ONLINE_NEWS = 'onlinenews'

# static list matching topics/info results
PLATFORM_SOURCE_PUSHSHIFT = 'pushshift'
PLATFORM_SOURCE_TWITTER = 'twitter'
PLATFORM_SOURCE_YOUTUBE = 'youtube'
PLATFORM_SOURCE_MEDIA_CLOUD = 'mediacloud'


def available_platforms() -> List[str]:
    return [
        PLATFORM_TWITTER + " / " + PLATFORM_SOURCE_TWITTER,
        PLATFORM_REDDIT + " / " + PLATFORM_SOURCE_PUSHSHIFT,
        PLATFORM_YOUTUBE + " / " + PLATFORM_SOURCE_YOUTUBE,
        PLATFORM_ONLINE_NEWS + " / " + PLATFORM_SOURCE_MEDIA_CLOUD,
    ]


def provider_for(platform: str, source: str) -> ContentProvider:
    """
    A factory method that returns the appropriate data provider. Throws an exception to let you know if the
    arguments are unsupported.
    :param platform: One of the PLATFORM_* constants above.
    :param source: One of the PLATFORM_SOURCE>* constants above.
    :return:
    """
    if (platform == PLATFORM_TWITTER) and (source == PLATFORM_SOURCE_TWITTER):
        platform_provider = TwitterTwitterProvider(TWITTER_API_BEARER_TOKEN)
    elif (platform == PLATFORM_REDDIT) and (source == PLATFORM_SOURCE_PUSHSHIFT):
        platform_provider = RedditPushshiftProvider()
    elif (platform == PLATFORM_YOUTUBE) and (source == PLATFORM_SOURCE_YOUTUBE):
        platform_provider = YouTubeYouTubeProvider(YOUTUBE_API_KEY)
    elif (platform == PLATFORM_ONLINE_NEWS) and (source == PLATFORM_SOURCE_MEDIA_CLOUD):
        platform_provider = OnlineNewsMediaCloudProvider(MEDIA_CLOUD_API_KEY)
    else:
        raise UnknownProviderException(platform, source)
    return platform_provider


class UnknownProviderException(Exception):
    def __init__(self, platform, source):
        super().__init__("Unknown provider {} from {}".format(platform, source))
