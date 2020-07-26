import pydub
import pydub.playback
import datetime
import os.path
import schedule
import time
import logging
import sys


AGITATION_TIME = '19:00'


def get_current_date_label():
    return str(datetime.date.today())


def get_play_list():
    audio_dir = os.path.join('playlist', get_current_date_label())
    if os.path.exists(audio_dir):
        return [os.path.join(audio_dir, x) for x in sorted(os.listdir(audio_dir))]
    else:
        return []


def agitate():
    logging.info('Agitation time!')
    play_list = get_play_list()
    for file in play_list:
        logging.info(f'Play {file}.')
        music = pydub.AudioSegment.from_file(file)
        pydub.playback.play(music)
    logging.info('Agitation is done!')


def setup_agitation_scheduler():
    schedule.every().day.at(AGITATION_TIME).do(agitate)


def poll_scheduler():
    logging.info('The system is in the scheduler loop.')
    while True:
        schedule.run_pending()
        time.sleep(1)


def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s  [%(levelname)s]  %(message)s', '%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)

    file_handler = logging.FileHandler('log.txt')
    file_handler.setFormatter(log_formatter)

    logger = logging.root
    logger.setLevel(logging.INFO)
    logger.handlers = [console_handler, file_handler]


def main():
    try:
        setup_logging()
        setup_agitation_scheduler()
        poll_scheduler()
    except KeyboardInterrupt:
        logging.info('Got keyboard interrupt.')
    finally:
        logging.info('Shutdown.')


if __name__ == '__main__':
    main()
