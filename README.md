Glimpse
=======

A prototype tool to give users a "glimpse" of attention on a platform based on a query with keywords and start/end
dates. Created to use in teaching as a temporary and exploratory solution. Right now this supports querying for the 
amount of attention on a number of platforms:
* Online news (via Media Cloud)
* Twitter (via their academic API track)
* YouTube (via their API)
* Reddit submissions (via Pushshift.io)

![Screenshot of glimpse tool, showing query interface and one chart of results](doc/screenshot.png?raw=true)

## Speculative Roadmap

This was a weekend project created to support teaching in a Digital Storytelling and Social Media class. Going forward,
it would make more sense to:
* implement a uniform "simple query" mode, so first-time users don't need to learn the query syntax specific to each 
platform
* try to determine a demoniator so we can show percentage of attention over time for each platform in one chart
* support filtering content by platform (ie. channels on Reddit, collectons of media sources for online news, etc)
* add support for more platforms via their APIs

## Installing

This requires installing redis (for caching results). Then:

```
pip3 install -r requirements
pip3 install click --upgrade
python3 -m spacy download en_core_web_sm
```

## Deploying to Dokku

1. `dokku apps:create glimpse`
2. `dokku redis:create glimpse-cache`
3. `dokku redis:link glimpse-cache glimpse`
4. `dokku config:set glimpse MC_API_KEY=keykeykey CACHE_REDIS_URL=urlurlurl TWITTER_API_BEARER_TOKEN=tokentoken YOUTUBE_API_KEY=keykey`
5. `dokku config:set --no-restart glimpse DOKKU_LETSENCRYPT_EMAIL=emailaddress`
6. `dokku ps:scale glimpse web=6`

## Running in Docker

```
docker image build -t glimpse .

docker container run --rm -it -p 8000:8000 -e MC_API_KEY=keykeykey -e CACHE_REDIS_URL=urlurlurl -e TWITTER_API_BEARER_TOKEN=tokentoken -e YOUTUBE_API_KEY=keykey glimpse
```

## Credits

Created by Rahul Bhargava, Assistant Professor of Journalism and Art + Design at Northeasern University.
* [Data Culture Group](https://dataculturegroup.org)
* [Media Cloud](https://mediacloud.org)
