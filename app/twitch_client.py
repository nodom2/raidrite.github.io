import logging
from app import settings
import requests
from app.auth import Auth
from abc import ABC, abstractmethod

module_logger = logging.getLogger(__name__+'.py')


def validate_name(given_name: str) -> dict:
    """This function validates a given_name using Twitch's API and returns a dictionary.

    :param str given_name: a streamer's name to be validated
    :return: a dictionary containing key-value pairs as: 'profile_img_url', 'display_name', 'login_name', 'twitch_uid',
    'broadcaster_type', and 'is_valid' (boolean value)
    :rtype: dict
    """
    if given_name is None:
        err_msg = "'given_name' supplied to validate_name() was 'None' type."
        module_logger.info("err_msg")
        raise ValueError(err_msg)

    if given_name == "":
        err_msg = "'given_name' supplied to validate_name() was empty: ('{}')".format(str(given_name))
        module_logger.info(err_msg)
        raise ValueError(err_msg)

    # Twitch API request parameters
    base_url = 'https://api.twitch.tv/helix/users'
    query_params = {'login': given_name.lower()}
    client_id = {'Client-ID': settings.TWITCH_CLIENT_ID}

    module_logger.info("Twitch API - 'validate_name()' for: " + '"{}"'.format(str(given_name)))
    # Request user information from Twitch API
    with requests.get(base_url, params=query_params, headers=client_id) as req:
        resp = req.json()['data']
        # Supplied name was found if len(resp['data'])  > 0
        if len(resp) == 0:
            err_msg = "Twitch API - 'validate_name()': Supplied name not found on Twitch: " + str(given_name)
            module_logger.info(err_msg)
            raise ValueError(err_msg)
        else:
            resp = resp[0]

        result = {
            'broadcaster_type': resp['broadcaster_type'],
            'profile_img_url':  resp['profile_image_url'],
            'display_name':     resp['display_name'],
            'name':             resp['login'],
            'twitch_uid':       resp['id'],
        }

    success_log_msg = "Twitch API - 'validate_name()' found user: "
    success_log_msg += '"{}" (twitch_uid: {})'.format(result['display_name'], result['twitch_uid'])
    module_logger.info(success_log_msg)
    return result


class TwitchAccount(ABC):
    """ Super Class for Twitch Accounts

    This class connects to the Twitch API to collect data for streamers and users.  Its primary purpose is to collect
    a list of *followers* for a Streamer or a list of *followings* for non-streamers (TwitchUser).  Results from this
    class can be used with the DB to lookup a user, add/update a user in the DB, and verify that DB records coincide
    with Twitch records (e.g., total_followers, or follow_list)
    """

    def __init__(self, auth=None):
        self.display_name = None
        self.name = None
        self.twitch_uid = None
        self.is_streamer = False
        self.twitch_follow_list = None

        # Set Authorization token from Twitch for API requests if not supplied
        if auth is None:
            self.twitch_auth = Auth(settings.TWITCH_CLIENT_ID, settings.TWITCH_CLIENT_SECR)

    @abstractmethod
    def get_total_follows_count(self):
        pass

    # TODO: This should be cleaned up by filtering out redundant fields in json response (e.g. for streamers,
    #  {kept_keys: follower[kept_keys] for kept_keys in ['followed_at', 'from_id', 'from_name']}
    def get_all_follows(self, given_uid: str, to_or_from_id: str, auth_bear_token: str) -> dict:
        """
        This function gets followers/followings for a given uid.  This works for collecting followers *to* a streamer
        as well as followings *from* general Twitch users.

        :param str given_uid: The uid whose followings will be collected
        :param str to_or_from_id: Either 'to_id' (for followers *to* a streamer) or 'from_id' (for followers *from*
        a regular user)
        :param str auth_bear_token: The authorization bearer token created by an Auth object; required for quick,
        repeated calls to Twitch API when collecting followers.
        :return: A dictionary containing 'total_followers' and 'n' keys for each 100 followings
        :rtype: dict
        """
        if auth_bear_token is None:
            err_msg = "'auth_bear_token' supplied to get_all_follows() was 'None' type."
            module_logger.info("err_msg")
            raise ValueError(err_msg)

        if auth_bear_token == "":
            err_msg = "'auth_bear_token' supplied to all_() was empty: ('{}')".format(str(auth_bear_token))
            module_logger.info(err_msg)
            raise ValueError(err_msg)

        # Twitch API request parameters
        base_url = 'https://api.twitch.tv/helix/users/follows'
        q_params = {to_or_from_id: given_uid, 'first': 100}
        bear_token = auth_bear_token

        module_logger.info('Twitch API - Collecting followers list for uid: {}'.format(str(given_uid)))
        # Create a new Session object for repeated requests to Twitch API
        with requests.Session() as sess:
            resp = sess.get(base_url, params=q_params, headers=bear_token).json()
            try:
                # Update pagination cursor for next 100
                q_params['after'] = resp['pagination']['cursor']
            except KeyError:
                # A nonfatal KeyError is thrown for the pagination cursor when user has zero followers
                pass
            # Get total from json response, irrespective of Streamer/non-Streamer self.total_followers
            total_follows = resp['total']
            # Get first 100 follows
            result = {'000': resp['data']}
            # Collect all remaining follows
            for next_100 in range(100, total_follows, 100):
                resp = sess.get(base_url, params=q_params, headers=bear_token).json()
                # Add next_100 key to results dict (like '100', '200', etc.)
                result[str(next_100)] = resp['data']
                # Update pagination cursor for next 100
                q_params['after'] = resp['pagination']['cursor']

        return result


class TwitchStreamer(TwitchAccount):

    def __init__(self, streamer_name: str):
        try:
            valid_streamer = validate_name(str(streamer_name))
        except ValueError as e:
            module_logger.info('Cannot create TwitchStreamer() object: Supplied name not valid ', e)
            return

        # Super class call
        super().__init__()
        # Set attributes using validate_name() results (a dict)
        for k, v in valid_streamer.items():
            setattr(self, k, v)

        # this field directs get_all_follows() to get a dict  of all *followers*
        self.to_from = 'to_id'
        self.is_streamer = True
        self.total_followers = self.get_total_follows_count()

        pass

    def get_total_follows_count(self) -> int:
        base_url = 'https://api.twitch.tv/helix/users/follows'
        query_params = {'to_id': self.twitch_uid, 'first': 1}
        client_id = {'Client-ID': self.twitch_auth.client_id}
        with requests.get(base_url, params=query_params, headers=client_id) as req:
            resp = req.json()['total']

        return resp

    def get_all_follows(self):
        if self.twitch_follow_list is None:
            module_logger.info('Streamer: No followers list set.  Collecting a list of ALL followers from Twitch...')
            self.twitch_follow_list = super().get_all_follows(self.twitch_uid, self.to_from, self.twitch_auth.bear_tok)

        return self.twitch_follow_list

class TwitchUser(TwitchAccount):

    def __init__(self, **kwargs):
        # Super class call
        super().__init__()

        # Set to_from field for get_all_follows: gets list of people this user *is following*
        self.to_from = 'from_id'
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)