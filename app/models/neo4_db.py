from app import settings
import logging
from app.twitch_client import TwitchStreamer
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, Label, RelatedTo, RelatedFrom

module_logger = logging.getLogger(__name__+'.py')

# for logging in fxn def outside class def
# https://docs.python.org/3/howto/logging-cookbook.html#using-logging-in-multiple-modules

graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD
)


class BaseModel(GraphObject):
    """Generic  base class for all py2neo/neo4j graph objects. """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def all(self):
        return self.match(graph)

    def save(self):
        graph.push(self)

# class User(BaseModel):
#     # The primary property key used for Cypher MATCH and MERGE operations
#     __primarykey__ = 'twitch_uid'
#     # The primary node label used for Cypher MATCH and MERGE operations
#     __primarylabel__ = 'User'
#
#     # PROPERTIES
#     twitch_uid = Property()
#     display_name = Property()
#
#     # RELATIONSHIPS
#     is_following = RelatedTo('Streamer', 'IS_FOLLOWING')
#     is_followed_by = RelatedFrom('User', 'IS_FOLLOWED_BY')


class User(BaseModel):
    # The primary property key used for Cypher MATCH and MERGE operations
    __primarykey__ = 'twitch_uid'

    # LABELS
    #   A Label defined on a GraphObject provides an accessor to a label of the underlying central node.
    #   It is exposed as a boolean value, the setting of which allows the label to be toggled on or off.
    streamer = Label('Streamer')

    # PROPERTIES
    twitch_uid = Property()
    name = Property()
    display_name = Property()
    profile_img_url = Property()
    broadcaster_type = Property()
    total_followers = Property()
    total_followings = Property()

    # RELATIONSHIPS
    # is_followed_by = RelatedFrom('User', 'IS_FOLLOWED_BY')
    # is_following = RelatedTo('User', 'IS_FOLLOWING')
    follows = RelatedTo('User', 'FOLLOWS')


def create_from_twitch_streamer(some_streamer: TwitchStreamer) -> User:
    db_streamer = None
    try:
        db_streamer = User()
        db_streamer.streamer = some_streamer.is_streamer
        db_streamer.twitch_uid = some_streamer.twitch_uid
        db_streamer.name = some_streamer.name
        db_streamer.display_name = some_streamer.display_name
        db_streamer.profile_img_url = some_streamer.profile_img_url
        db_streamer.broadcaster_type = some_streamer.broadcaster_type
        db_streamer.total_followers = some_streamer.total_followers
        db_streamer.save()
        module_logger.info("Added {} to DB".format(some_streamer.display_name))

    except Exception as exc:
        module_logger.error("Failed to add streamer to db:  {}".format(some_streamer.display_name))
        module_logger.error(exc)

    return db_streamer

# TODO: Refactor so that this work with TwitchStreamer or TwitchUser objects (refactor to_from in these classes')
# TODO: If creatinga "streamer set" from this result, then we do not need to return a dict (only a list/set of followers)
def add_all_followers(some_streamer: TwitchStreamer, db_streamer: User) -> dict:
    """
    Adds all followers to db for a given TwitchAccount object and py2neo ogm object
    :param some_streamer:
    :param db_streamer:
    :return:
    """
    foll_list = some_streamer.get_all_follows()
    to_from = some_streamer.to_from
    # A dictionary of {'twitch_uid': db_object}; useful for adding follower's followings
    #all_db_folls_dict = {}


    for each_hundred_list in foll_list.keys():
        for each_fol in foll_list[each_hundred_list]:
            db_follower = User()
            try:
                db_follower.twitch_uid = each_fol['from_id']
                #db_follower.display_name = each_fol['from_name']   # breaks on names like '抜け' without unicode encoding
                db_follower.follows.add(db_streamer, properties={'followed at': each_fol['followed_at']})
                # Commit to new follower to DB
                db_follower.save()
            except Exception as exc:
                module_logger.error("Failed to add follower to db: {}".format(each_fol['from_name']))
                module_logger.error(exc)

            #all_db_folls_dict[db_follower.twitch_uid] = db_follower

    return foll_list


def get_streamer_set_from_foll_dict(db_folls_dict: dict):
    """
    Takes a dictionary of {twitch_uid: db_follower} and creates a set of streamers that all followers follow

    :param db_folls_dict:
    :return:
    """
    all_streamers = {}

    for each_foll_id in db_folls_dict.keys():
        # Get a list of who a follower follows & add it to all_streamers list
        pass