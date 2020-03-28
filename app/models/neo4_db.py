from app import settings
import logging
import app.twitch_client as twitch_client
from app.twitch_client import TwitchStreamer
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, Label, RelatedFrom

module_logger = logging.getLogger(__name__+'.py')

# for logging in fxn def outside class def
# https://docs.python.org/3/howto/logging-cookbook.html#using-logging-in-multiple-modules
# TODO: This may need to move to an extensions.py file and imported here so that new DB connections will not be made for
#  each instantiation of this class (from extensions import graph)
graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD
)

graph.schema.create_uniqueness_constraint('User', 'twitch_uid')
graph.schema.create_uniqueness_constraint('Streamer', 'twitch_uid')


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


class User(BaseModel):
    """
    Constructs an abstract representation (GraphObject) of a record in database, a User Node.   Can be used with `Graph`
    to match, update, or create a record in the neo4j DB.   The streamer `Label` is a boolean value that allows the
    "Streamer" label to be toggled on/off for a Node.  By default, GraphObjects represent User nodes.  A `Relationship`
    describes how User and Streamer nodes are associated.

    """
    # The primary property key used for Cypher MATCH and MERGE operations
    __primarykey__ = 'twitch_uid'

    # PROPERTIES
    twitch_uid = Property()
    name = Property()
    display_name = Property()
    profile_img_url = Property()
    broadcaster_type = Property()
    total_followers = Property()
    total_followings = Property()

    # LABELS
    #  A Label defined on a GraphObject provides an accessor to a label of the underlying central node.
    #  It is exposed as a boolean value, the setting of which allows the label to be toggled on or off.
    streamer = Label('Streamer')

    # RELATIONSHIPS
    is_followed_by = RelatedFrom('User', 'FOLLOWS')

    @staticmethod
    def create_or_update_from_twitch_client(some_streamer: TwitchStreamer):
        db_streamer = User()
        try:
            for key, val in some_streamer.as_dict().items():
                db_streamer.__setattr__(key, val)
            # TODO: Note that this updates an existing node; this may be undesirable if we want to compare
            #  total followers reported by Twitch to record in DB and perform an action
            # Add or Update in DB
            db_streamer.save()
            module_logger.info("Added {} to DB".format(some_streamer.display_name))
        except Exception as exc:
            module_logger.error("Failed to add streamer to db:  {}".format(some_streamer.display_name))
            module_logger.error(exc)

        return db_streamer

    @staticmethod
    def add_followers_to_streamer(some_streamer: TwitchStreamer, db_streamer: GraphObject) -> dict:
        """
        Adds all followers to db for a given TwitchStreamer object and py2neo ogm object

        :param some_streamer: TwitchStreamer object and related methods
        :param db_streamer: An GraphObject representation of a Streamer node in the DB
        :return: List of follower id's obtained from twitch
        """
        foll_list = some_streamer.get_all_follows()
        foll_nodes = []

        for each_fol in foll_list:
            db_follower = User()
            try:
                db_follower.twitch_uid = each_fol['from_id']
                db_follower.display_name = each_fol['from_name']
                # Commit to new follower to DB
                db_follower.save()
                foll_nodes.append(db_follower)
                # Add Followed-by relationship to Streamer Node
                db_streamer.is_followed_by.update(
                    db_follower, properties={'followed at': each_fol['followed_at']}
                )

            except Exception as exc:
                module_logger.error("Failed to add follower to db: {}".format(each_fol['from_name']))
                module_logger.error(exc)
                pass

        # Save all updated follower references to DB
        db_streamer.save()
        # Return a list of follower id's from twitch
        return {'foll_id_list': [each_fol['from_id'] for each_fol in foll_list], 'foll_nodes': foll_nodes}

    @staticmethod
    def add_all_followers_followings(foll_dict: dict):
        for follower_id, foll_node in zip(foll_dict['foll_id_list'], foll_dict['foll_nodes']):
            # Fetch a followings list from twitch
            all_followings = twitch_client.get_all_follows(follower_id, 'from_id', skip_validation=True)

            for some_followed_stream in all_followings:
                # Attempt to find Streamer node in DB
                matched_streamer = User.match(graph, some_followed_stream['to_id']).first()

                if matched_streamer is None:
                    new_streamer = TwitchStreamer(some_followed_stream['to_name'])
                    matched_streamer = User.create_or_update_from_twitch_client(new_streamer)

                matched_streamer.is_followed_by.update(
                    foll_node, properties={'followed at': some_followed_stream['followed_at']}
                )
                matched_streamer.save()

# TODO: Delete or move this to twitch client?  it performs ZERO db operations
# def get_streamer_set_from_foll_list(streamers_foll_list: list):
#     """
#     Takes a list of twitch_ud (followers) and returns a list of streamer names that all users follow
#
#     :param streamers_foll_list: List of user id's to determine their followings
#     :return: List of unique streamer names that all users in list follow
#     """
#     all_streamers = set()
#     dont_validate_auth_token = True
#
#     for each_foll_id in streamers_foll_list:
#         # Get a list of who a follower follows & add it to all_streamers list
#         for each_streamer in twitch_client.get_all_follows(each_foll_id, 'from_id', dont_validate_auth_token):
#             all_streamers.add(each_streamer['to_name'])
#
#     try:
#         all_streamers.remove('')
#     except:
#         pass
#
#     return list(all_streamers)
