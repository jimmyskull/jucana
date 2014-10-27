# -*- coding: utf-8 -*-
import os.path
import sys
import time

import json

class ExampleProcessor(object):
    '''Barebone for a processor class'''
    
    def __init__(self, tweet_count):
        '''|tweet_count| is the total number of calls to |tweet()| until
        finish and call |done()|'''
        pass

    def tweet(self, json_object):
        '''Process one tweet. |json_object| is structured according to
        http://dev.datasift.com/docs/getting-started/data/twitter'''
        pass

    def done(self):
        '''After processing all tweets, |done()| is called to do some
        after work, like generating the desired output.'''
        pass

class RetweetTest(object):
    '''Test that only count the number of retweets with a specific hashtag'''
    def __init__(self, tweet_count):
        self.count = 0
        self.tweet_count = tweet_count

    def tweet(self, json_object):
        tweet = json_object['interaction']['content'].lower()
        if '#debatenaglobo' in tweet and 'retweet' in json_object['twitter']:
            self.count += 1

    def done(self):
        ratio = self.count * 100.0 / self.tweet_count
        print 'Selected {} tweets ({:.1f}%)'.format(self.count, ratio)

class Status(object):
    def __init__(self, total):
        self.start = time.time()
        self.count = 0
        self.total_count = 0
        self.total = total

    def update_status(self):
        self.count += 1
        self.total_count += 1
        if time.time() - self.start < 1.0:
            return
        progress = 100.0 * self.total_count / self.total
        print '\r{:.1f}%  {} tweets/sec '.format(progress, self.count), 
        sys.stdout.flush()
        self.count = 0
        self.start = time.time()


def run(f, Processor):
    print 'Loading input file...'
    lines = f.readlines()
    size = len(lines)
    print 'Processing {} tweets...'.format(size)
    processor = Processor(size)
    status = Status(size)
    for line in lines:
        obj = json.loads(line)
        processor.tweet(obj)
        status.update_status()
    print
    processor.done()

FILE = 'twitter.json'
if not os.path.isfile(FILE):
    print 'File {} not found.'.format(FILE)
    exit(1)

with open('twitter.json', 'r') as f:
    import retweet
    #run(f, retweet.RetweetActivity)
    run(f, retweet.RetweetGraph)
    #run(f, RetweetTest)

