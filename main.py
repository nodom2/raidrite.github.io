from app.twitch_client import TwitchStreamer
from app.models import neo4_db
import logging
import time

# Create a new logger instance for this application
logger = logging.getLogger()


# This is just a demo; also useful for debugging.
def main():
    start_time = time.time()
    # Get (validated) details about a streamer from twitch, given a streamer name
    some_twitch_streamer = TwitchStreamer('stroopC')
    # Add streamer to db
    db_streamer = neo4_db.create_from_twitch_streamer(some_twitch_streamer)
    # Add all follower relationships to graph, get list of twitch uid's for followers
    added_foll_id_list = neo4_db.add_all_followers(some_twitch_streamer, db_streamer)
    # Get a list of all streams that followers are following
    all_followed_streams = neo4_db.get_streamer_set_from_foll_list(added_foll_id_list)

    # TODO: IMPLEMENT SHARED SESSIONS FOR ALL REQUESTS
    print("")
    for streamer_name in all_followed_streams:
        # Get (validated) details about a streamer from twitch, given a streamer name
        new_streamer = TwitchStreamer(streamer_name)
        # Add new streamer to db
        new_db_streamer = neo4_db.create_from_twitch_streamer(new_streamer)
        # Add all follower relationships to graph
        neo4_db.add_all_followers(new_streamer, new_db_streamer)

    print("--- %s seconds ---" % (time.time() - start_time))


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
