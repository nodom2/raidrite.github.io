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
    db_streamer = neo4_db.User.create_or_update_from_twitch_client(some_twitch_streamer)
    # Add all follower relationships to graph, get dict of foll twitch_uid and foll_nodes
    added_folls_dict = db_streamer.add_followers_to_streamer(some_twitch_streamer, db_streamer)
    # Add all followers followings to DB
    db_streamer.add_all_followers_followings(added_folls_dict)

    print("--- %s seconds ---" % (time.time() - start_time))


def logging_setup():
    # logger = logging.getLogger()
    # Set the logging level for this application
    logger.setLevel(logging.DEBUG)

    # Create file handler which logs event debug messages
    log_file_path = 'logs/main.py.log'
    fh = logging.FileHandler(log_file_path, encoding="'utf-8'")
    fh.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

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
