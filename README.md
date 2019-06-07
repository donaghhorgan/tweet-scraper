# tweet-scraper

A command line wrapper for [tweepy's](https://tweepy.readthedocs.io/en/latest/) search function. Writes tweet JSON to a [JSON Lines](http://jsonlines.org/) format file. Waits when the rate limit is hit for larger scale queries. 

## Prerequisites

Dependencies are managed with [pipenv](https://pipenv.readthedocs.io/en/latest/). Run `pipenv install` to create a virtual environment with the packages you need to run the scraper.

## Usage

### API credentials

tweet-scraper looks for API credentials in the following environment variables: `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN` and `TWITTER_ACCESS_TOKEN_SECRET`. If all four variables are defined, then OAuth authentication will be used. Otherwise, app authentication will be attempted with just `TWITTER_CONSUMER_KEY` and `TWITTER_CONSUMER_SECRET`.

If you define the credentials in a `.env` file, pipenv will automatically load them into the environment before running the scraper.

### General usage

The simplest use is just dumping some query results to a file:

```bash
pipenv run ./scrape.py -q 'hello world' -o hello_world.jsonLoading .env environment variables…
[2019-06-07 18:55:28,954]: Using OAuth authentication
[2019-06-07 18:55:29,682]: Dumping page 1 to hello_world.json
[2019-06-07 18:55:30,194]: Dumping page 2 to hello_world.json
[2019-06-07 18:55:30,692]: Dumping page 3 to hello_world.json
...
```

More sophisticated queries are possible though. Most API options are supported:

```bash
$ pipenv run ./scrape.py -h
Loading .env environment variables…
usage: scrape.py [-h] [-e] [-r RESULT_TYPE] [--lang LANG] [--locale LOCALE]
                 [--count COUNT] [--page PAGE] [--since SINCE] [--until UNTIL]
                 [--since_id SINCE_ID] [--max_id MAX_ID] [--geocode GEOCODE]
                 [--show_user SHOW_USER] -q Q -o FILENAME

Scrape tweets and dump them to a file.

optional arguments:
  -h, --help            show this help message and exit
  -e, --tweet_mode      include the full text of tweets longer than 140
                        characters
  -r RESULT_TYPE, --result_type RESULT_TYPE
                        the type of search results (default: recent)
  --lang LANG           the language to restrict search results to
  --locale LOCALE       the language of the query you are sending
  --count COUNT         the number of tweets to return per page (default: 100)
  --page PAGE           the starting page number to return
  --since SINCE         scrape statuses more recent than this date (YYYY-MM-DD
                        format)
  --until UNTIL         scrape statuses less recent than this date (YYYY-MM-DD
                        format)
  --since_id SINCE_ID   scrape statuses with an ID greater (that is, more
                        recent) than this
  --max_id MAX_ID       scrape statuses with an ID less (that is, less recent)
                        than this
  --geocode GEOCODE     scrape tweets by users located within the given
                        latitude/longitude/radius
  --show_user SHOW_USER
                        prepends “<user>:” to the beginning of tweets
  -q Q, --query Q       the query to run
  -o OUTPUT, --output OUTPUT
                        the file to dump tweet data to
```

Further information on the query parameters is available in the [tweepy documentation](https://tweepy.readthedocs.io/en/latest/index.html) and the [Twitter API documentation](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets).