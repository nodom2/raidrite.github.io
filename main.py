from app.twitch_client import TwitchStreamer, TwitchAccount, TwitchUser
from app.models import neo4_db
import logging

# Create a new logger instance for this application
logger = logging.getLogger()

# This is just a demo; also useful for debugging.
def main():
    # Get info about a streamer from twitch
    tmp_twitch_streamer = TwitchStreamer('stroopC')
    db_streamer = neo4_db.create_from_twitch_streamer(tmp_twitch_streamer)
    added_folls_dict = neo4_db.add_all_followers(tmp_twitch_streamer, db_streamer)

    # For each follower in added_folls_dict, get a list of who they follow
    
    
    #fols = tmp_twitch_streamer.get_all_follows()

    #for each_hundred_list in fols.keys():
        #print(fols[each_hundred_list])


    def add_to_db(TwitchStreamer):
        db_streamer = neo4_db.User()
        db_streamer.streamer = True
        db_streamer.twitch_uid = TwitchStreamer.twitch_uid
        db_streamer.name = TwitchStreamer.name
        db_streamer.display_name = TwitchStreamer.display_name
        db_streamer.profile_img_url = TwitchStreamer.profile_img_url
        db_streamer.broadcaster_type = TwitchStreamer.broadcaster_type
        db_streamer.total_followers = TwitchStreamer.total_followers
        #db_streamer.save()

        foll_list = TwitchStreamer.get_all_follows()
        foll_ids = ''

        for each_hundred_list in foll_list.keys():
            for each_fol in foll_list[each_hundred_list]:
                db_foll = neo4_db.User()
                db_foll.twitch_uid = each_fol['from_id']
                #db_foll.display_name = each_fol['from_name']   # breaks on names like '抜け' without unicode encoding
                #db_streamer.is_followed_by.add(db_foll,properties={'followed at': each_fol['followed_at']})
                db_foll.follows.add(db_streamer, properties={'followed at': each_fol['followed_at']})
                db_foll.save()
                foll_ids += each_fol['from_id']

        #db_streamer.save()

    add_to_db(tmp_twitch_streamer)




    print("")
    #db = neo4_db.Neo4jDB()
    #db.find_or_add_streamer('stroopc')
    #folls = tmp_twitch_streamer.get_all_follows()
    #streamer_node = db.create_streamer_node(tmp_twitch_streamer)
    #db.add_streamer_folls_from_twitch(tmp_twitch_streamer, streamer_node)




def logging_setup():
    # logger = logging.getLogger()
    # Set the logging level for this application
    logger.setLevel(logging.DEBUG)

    # Create file handler which logs event debug messages
    log_file_path = 'logs/main.py.log'
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # Create a formatter
    log_display_format = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=log_display_format, datefmt=log_date_format)

    # Add formatter to handlers
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Add Starting Message and Line Break
    logger.warning('Starting new run of {}'.format(__name__))


if __name__ == "__main__":
    logging_setup()
    main()
