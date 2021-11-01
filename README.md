Glimpse
=======

A prototype tool to give users a "glimpse" of attention on a platform based on a query with keywords and start/end
dates. Created to use in teaching as a temporary and exploratory solution.


## Installing:

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
