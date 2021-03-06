import asyncio
import time

from loguru import logger

from config import logger_config_for_core
from utils.functions import notice
from utils.tasks import checking_bots, update_user_data, checking_users_tasks, \
    creating_club_tasks


async def main():
    methods = [update_user_data(), checking_bots(), checking_users_tasks(),
               creating_club_tasks()]
    tasks = []
    for method in methods:
        task = asyncio.create_task(method)
        tasks.append(task)

    responses = asyncio.gather(*tasks)
    await responses


if __name__ == '__main__':
    # Настройка логгера
    logger.configure(**logger_config_for_core)
    logger.enable("")
    logger.success("Ядро запущено.")
    noticed = False
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logger.critical(f"MpetsCore down. {e}")
            if not noticed:
                text = "MpetsCore down. \n"\
                       "Please check the error information "\
                       "in the log files. @wilidon"
                notice(message=text)
            noticed = True
        time.sleep(10)
