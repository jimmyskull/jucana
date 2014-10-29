# -*- coding: utf-8 -*-

from time import strptime, mktime

import itertools

class RetweetGraph(object):
    '''Build a graph based on hashtags.'''

    new_id = itertools.count(1).next

    def __init__(self, tweet_count, hashtag='#DebateNaGlobo'):
        self.users = dict()
        self.users_id = dict()
        self.links = dict()
        self.selected_count = 0
        self.tweet_count = tweet_count
        self.hashtag = hashtag.lower()

    def add_user(self, user):
        if user in self.users:
            u = self.users[user]
            u['activity'] += 1
        else:
            i = self.new_id()
            self.users[user] = dict(id=i, activity=1)
            self.users_id[i] = user
            
    def add_edge(self, user1, user2):
        self.add_user(user1)
        self.add_user(user2)
        e = frozenset([user1, user2])
        if e not in self.links:
            self.links[e] = 1
        else:
            self.links[e] += 1

    def tweet(self, json_object):
        #if len(self.users) >= 1000:
        #    return
        tweet = json_object['twitter']
        retweet = 'text' not in tweet
        if retweet:
            content = tweet['retweet']['text'].lower()
        else:
            return
            content = tweet['text'].lower()
        if self.hashtag not in content:
            return
        self.selected_count += 1
        if retweet:
            # Nodes: User id
            a = int(tweet['retweet']['user']['id'])
            b = int(tweet['retweeted']['user']['id'])
            # Nodes: Tweet id
            #a = int(tweet['retweet']['id'])
            #b = int(tweet['retweeted']['id'])
            self.add_edge(a, b)
        else:
            author = int(tweet['user']['id'])
            self.add_user(author)

    def done(self):
        ratio = self.selected_count * 100.0 / self.tweet_count
        print 'Valid tweets: {} ({:.2f}%)'.format(self.selected_count, ratio)
        print 'Users: {}'.format(len(self.users))
        print 'Links: {}'.format(len(self.links))
        print 'Generating graph file...'
        self.generate()
        print 'Done.'

    def generate(self):
        fn = self.hashtag[1:] + '_graph.net'
        print fn
        with open(fn, 'w') as f:
            f.write('*Vertices {}\n'.format(len(self.users)))
            for index in range(1, len(self.users) + 1):
                uid = self.users_id[index]
                u = self.users[uid]
                f.write('{} "{}" size {}\n'.format(u['id'], uid, u['activity']))
            f.write('*Arcs\n')
            for u in self.links.keys():
                id_a, id_b = u
                a, b = self.users[id_a]['id'], self.users[id_b]['id']
                weight = self.links[u]
                f.write('{} {} {}\n'.format(a, b, weight))

class RetweetActivity(object):
    '''Build a graph based on hashtags.'''

    output_file = 'activity.table'
    new_id = itertools.count(1).next

    def __init__(self, tweet_count, hashtag='#DebateNaGlobo'):
        self.bin_size = 60
        self.selected_count = 0
        self.tweet_count = tweet_count
        self.hashtag = hashtag.lower()
        self.start = mktime(strptime("Fri, 24 Oct 2014 09:00:59 +0000", "%a, %d %b %Y %H:%M:%S +0000"))
        self.bins = dict()

    def tweet(self, json_object):
        tweet = json_object['twitter']
        retweet = 'text' not in tweet
        if retweet:
            return
            content = tweet['retweet']['text'].lower()
        else:
            #return
            content = tweet['text'].lower()
        if self.hashtag not in content:
            return
        self.selected_count += 1
        if 'created_at' in tweet:
            created_at = tweet['created_at']
        else:
            created_at = tweet['retweet']['created_at']
        t = mktime(strptime(created_at, "%a, %d %b %Y %H:%M:%S +0000"))
        elapsed = t - self.start
        if elapsed < 0.0:
            print 'Ignored', created_at, elapsed
            return
        b = round(elapsed / self.bin_size)
        if b in self.bins:
            self.bins[b] += 1
        else:
            self.bins[b] = 1

    def generate(self):
        with open(self.output_file, 'w') as f:
            for k, v in self.bins.iteritems():
                f.write('{} {}\n'.format(int(k), int(v)))

    def done(self):
        ratio = self.selected_count * 100.0 / self.tweet_count
        print 'Valid tweets: {} ({:.2f}%)'.format(self.selected_count, ratio)
        print 'Bins: {}'.format(len(self.bins))
        print 'Generating file {}'.format(self.output_file)
        self.generate()
        print 'Done.'

