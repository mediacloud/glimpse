import logging
from typing import List
import os
from pathlib import Path

from .. import YOUTUBE_API_KEY, TWITTER_API_BEARER_TOKEN, MEDIA_CLOUD_API_KEY
from .provider import ContentProvider
from .reddit import RedditPushshiftProvider
from .twitter import TwitterTwitterProvider
from .youtube import YouTubeYouTubeProvider
from .onlinenews import OnlineNewsMediaCloudProvider, OnlineNewsWaybackMachineProvider

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
PLATFORM_SOURCE_WAYBACK_MACHINE = 'waybackmachine'


def available_platforms() -> List[str]:
    return [
        PLATFORM_TWITTER + " / " + PLATFORM_SOURCE_TWITTER,
        PLATFORM_REDDIT + " / " + PLATFORM_SOURCE_PUSHSHIFT,
        PLATFORM_YOUTUBE + " / " + PLATFORM_SOURCE_YOUTUBE,
        PLATFORM_ONLINE_NEWS + " / " + PLATFORM_SOURCE_MEDIA_CLOUD,
        PLATFORM_ONLINE_NEWS + " / " + PLATFORM_SOURCE_WAYBACK_MACHINE,
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
    elif (platform == PLATFORM_ONLINE_NEWS) and (source == PLATFORM_SOURCE_WAYBACK_MACHINE):
        platform_provider = OnlineNewsWaybackMachineProvider()
    else:
        raise UnknownProviderException(platform, source)
    return platform_provider


class UnknownProviderException(Exception):
    def __init__(self, platform, source):
        super().__init__("Unknown provider {} from {}".format(platform, source))
