import tweepy
import logging

# must be better
logging.basicConfig(level=logging.DEBUG)


class twitterClient(object):

    def __init__(self, config_dict=False):

        self.t_acc_token = config_dict['t_acc_token']
        self.t_acc_secret = config_dict['t_acc_secret']
        self.t_api_key = config_dict['t_api_key']
        self.t_api_secret = config_dict['t_api_secret']

    def connect(self):
        auth = tweepy.OAuthHandler(self.t_api_key, self.t_api_secret)
        auth.set_access_token(self.t_acc_token, self.t_acc_secret)

        api = tweepy.API(auth)

        return api

    def fetch(self, todo):
        fetched = []

        for el in todo:
            api = self.connect()
            results = api.search(q=el['hashtag'])

            logging.debug("Fetching data for #%s" % el['hashtag'])

            for r in results:
                hashtags = []
                for h in r.entities['hashtags']:
                    hashtags.append({'tag': h['text']})

                data = {'oid': r.id,
                        'text': r.text,
                        'author': r.author.screen_name,
                        'avatar': r.user.profile_image_url_https,
                        'hashtags': hashtags,
                        'created_at': r.created_at}

                fetched.append(data)

        return fetched
