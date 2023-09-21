import logging
import os
import sys
import time
from http import HTTPStatus
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] func %(funcName)s(%(lineno)d): %(message)s'
)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000,
                              backupCount=5)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_tokens():
    """Проверяем доступность переменных."""
    return all([PRACTICUM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN])


def send_message(bot, message):
    """Отправление сообщений в чат."""
    logger.info(f'Отправляем сообщение: {message}')
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
    except Exception as error:
        logging.error('Ошибка отправки сообщения в Telegram')
        raise exceptions.ChatNotFoundException(error)
    else:
        logging.debug('Сообщение успешно отправлено в Telegram')


def get_api_answer(current_timestamp):
    """Делам запрос к эндпоинту."""
    timestamp = current_timestamp or int(time.time())
    params = dict(
        url=ENDPOINT,
        headers=HEADERS,
        params={"from_date": timestamp}
    )
    logger.info('Делам запрос к эндпоинту')
    try:
        homework_statuses = requests.get(**params)
    except Exception as error:
        logging.error(f"Ошибка при запросе к API: {error}")
    else:
        if homework_statuses.status_code != HTTPStatus.OK:
            error_message = "Статус страницы не равен 200"
            raise requests.HTTPError(error_message)
        return homework_statuses.json()
    logging.debug('Запрос к эндпоинту выполнен!')


def check_response(response):
    """Проверяем корректность ответа."""
    logging.info('Ответ от сервера получен')
    if not isinstance(response, dict):
        raise TypeError(f'Ответ API возвращает {type(response)} вместо dict')
    if response.get('current_date') is None:
        raise exceptions.CurrentDateError(
            'В ответе API отсутствует ключ current_date')
    homeworks = response.get('homeworks')
    if homeworks is None:
        raise KeyError('В ответе API отсутствует ключ homework')
    if not isinstance(homeworks, list):
        raise TypeError(
            f'В ответе API homework является {type(homeworks)} вместо list'
        )
    return homeworks


def parse_status(homework):
    """Извлекаем статус работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        raise KeyError('В ответе API отсутствует ключ homework_name')
    if homework_status not in HOMEWORK_VERDICTS:
        raise KeyError(f'Статус {homework_status} не найден')
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Ошибка в получении токенов!')
        sys.exit()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            current_timestamp = response.get('current_date', int(time.time()))
            homeworks = check_response(response)
            if len(homeworks) > 0:
                send_message(bot, parse_status(homeworks[0]))
        except exceptions.NoMessageToTelegram as error:
            logger.error(f'Сбой в работе программы: {error}', exc_info=True)
        except exceptions.EndPointIsNotAvailiable as error:
            logger.error(f"Недоступен API {error}")
            send_message(bot, f"API недоступно {error}")
        except exceptions.TokenNotFoundException as error:
            message = f"Отсутствует Token {error}"
            logger.error(message)
            send_message(bot, message)
        except exceptions.ChatNotFoundException as error:
            message = f"Отсутствует CHAT_ID {error}"
            logger.error(message)
            send_message(bot, message)
        except TypeError as error:
            message = f"Неправильный формат данных {error}"
            logger.error(message)
            send_message(bot, message)
        else:
            logger.debug("Ошибки отсутствуют!")
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
