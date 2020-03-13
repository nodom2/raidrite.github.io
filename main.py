from app import neo4_db
from app.twitch_client import TwitchStreamer
import logging

# Create a new logger instance for this application
logger = logging.getLogger()


def main():
    # Get info about a streamer from twitch
    tmp_twitch_streamer = TwitchStreamer('stroopC')
    fols = tmp_twitch_streamer.get_all_follows()

    for each_hundred_list in fols.keys():
        print(fols[each_hundred_list])

    #db = neo4_db.Neo4jDB()
    #db.find_or_add_streamer('stroopc')
    #folls = tmp_twitch_streamer.get_all_follows()
    #streamer_node = db.create_streamer_node(tmp_twitch_streamer)
    #db.add_streamer_folls_from_twitch(tmp_twitch_streamer, streamer_node)

    pass


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
