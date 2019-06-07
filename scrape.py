#! /usr/bin/env python
import argparse
import logging
import json
import os

import tweepy

# Override these API defaults to more sensible values for a scraper
RESULT_TYPE = 'recent'
COUNT = 100

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Scrape tweets and dump them to a file.')
    parser.add_argument('-e', '--tweet_mode', action='append_const', const='extended',
                        help='include the full text of tweets longer than 140 characters')
    parser.add_argument('-r', '--result_type', default=RESULT_TYPE,
                        help='the type of search results (default: {})'.format(RESULT_TYPE))
    parser.add_argument('--lang',
                        help='the language to restrict search results to')
    parser.add_argument('--locale',
                        help='the language of the query you are sending')
    parser.add_argument('--count', type=int, default=COUNT,
                        help='the number of tweets to return per page (default: {})'.format(COUNT))
    parser.add_argument('--page', type=int,
                        help='the starting page number to return')
    parser.add_argument('--since',
                        help='scrape statuses more recent than this date (YYYY-MM-DD format)')
    parser.add_argument('--until',
                        help='scrape statuses less recent than this date (YYYY-MM-DD format)')
    parser.add_argument('--since_id',
                        help='scrape statuses with an ID greater (that is, more recent) than this')
    parser.add_argument('--max_id',
                        help='scrape statuses with an ID less (that is, less recent) than this')
    parser.add_argument('--geocode',
                        help='scrape tweets by users located within the given latitude/longitude/radius')
    parser.add_argument('--show_user',
                        help='prepends “<user>:” to the beginning of tweets', default=False)
    parser.add_argument('-q', '--query', dest='q', required=True,
                        help='the query to run')
    parser.add_argument('-o', '--output', required=True,
                        help='the file to dump tweet data to')
    args = vars(parser.parse_args())

    output = args.pop('output')

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

    # Configure the API auth
    if 'TWITTER_ACCESS_TOKEN' in os.environ and 'TWITTER_ACCESS_TOKEN_SECRET' in os.environ:
        logging.info('Using OAuth authentication')
        auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
        auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    else:
        logging.info('Using app authentication')
        auth = tweepy.AppAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Run the query
    cursor = tweepy.Cursor(api.search, **{k: v for k, v in args.items() if v is not None})

    for i, page in enumerate(cursor.pages(), start=1):
        logging.info('Dumping page {} to {}'.format(i, output))

        with open(output, 'a') as f:
            for tweet in page:
                json.dump(tweet._json, f)
                f.write('\n')
