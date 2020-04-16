from operator import itemgetter
import logging
import queue
import requests
from multiprocessing.pool import ThreadPool
import time
import threading

from django.conf import settings as settings
from ..common.constants import DPOW_DELAY
from ..common.retry import retry

from .account_service import AccountService


logger = logging.getLogger(__name__)


class POWService:
    _pow_queue = queue.Queue()
    _running = False
    thread_pool = None
    loop = None
    thread = None

    @classmethod
    def in_queue(cls, account):
        temp_queue = cls.queue_to_list()
        for item in temp_queue:
            if item[0] == account:
                return True
        return False

    @classmethod
    def put_account(cls, account, frontier):
        in_time = int(round(time.time() * 1000))
        cls._pow_queue.put((account, frontier, in_time))

    @classmethod
    def get_account(cls):
        temp_queue = cls.queue_to_list()
        temp_queue = sorted(temp_queue, key=itemgetter(2))

        head = temp_queue[0]
        if head[2] + DPOW_DELAY <= int(round(time.time() * 1000)):
            copy_queue = queue.Queue()
            [copy_queue.put(i) for i in temp_queue[1:]]
            cls._pow_queue = copy_queue
            return head[0], head[1]

    @classmethod
    def is_empty(cls):
        temp_queue = cls.queue_to_list()
        temp_queue = sorted(temp_queue, key=itemgetter(2))

        if len(temp_queue) > 0 and temp_queue[0][2] + DPOW_DELAY * 1000 <= int(round(time.time() * 1000)):
            return False
        return True

    @classmethod
    def queue_to_list(cls):
        temp_list = []
        for i in cls._pow_queue.queue:
            temp_list.append(i)
        return temp_list

    @classmethod
    def get_pow(cls, account, hash_value):
        POW = None
        try:
            POW = retry(lambda: cls._get_dpow(hash_value)['work'], retries=5, pause=.5)
        except:
            logger.error('dPoW failure account %s' % account.address)

        if POW is None:
            account.unlock()
            logger.exception('dPoW get failure account %s unlocked without PoW' % account.address)
            raise Exception()

        return POW

    @classmethod
    def _get_dpow(cls, hash_value):
        data = {
            "user": settings.DPOW_API_USER,
            "api_key": settings.DPOW_API_KEY,
            "multiplier": 4.0,  ##4x base
            "hash": hash_value,
        }

        res = retry(lambda: requests.post(url=settings.DPOW_ENDPOINT, json=data, timeout=15))
        logger.info('dPoW Status %s %s' % (res.status_code, res.json()))

        if res.status_code == 200:
            return res.json()
        else:
            logger.exception('dPoW Status %s %s' % (res.status_code, res.json()))
            raise Exception()

    @classmethod
    def _run(cls):
        while cls._running:
            while not cls.is_empty():
                account, frontier = cls.get_account()

                try:
                    account.POW = cls.get_pow(account=account, hash_value=frontier)
                    logger.info('Generated POW: %s for account %s' % (account.POW, account.address))
                    time.sleep(.1)  ## Don't spam dPoW

                    account.unlock()
                except Exception as e:
                    logger.exception('Exception in POW thread: %s ' % e)
                    logger.exception('dPoW failure account %s unlocked without PoW' % account.address)
                    account.unlock()
            time.sleep(.1)

    @classmethod
    def enqueue_account(cls, account, frontier):
        logger.info('Enqueuing address %s frontier %s' % (account.address, frontier))
        account.lock()
        cls.put_account(account, frontier)

    @classmethod
    def start(cls, daemon=True):
        if not cls._running:
            cls._running = True

            logger.info('Starting PoW thread.')

            cls.thread_pool = ThreadPool(processes=4)
            cls.thread = threading.Thread(target=cls._run)
            cls.thread.daemon = daemon
            cls.thread.start()

    @classmethod
    def stop(cls):
        logger.info('Stopping PoW thread.')
        cls._running = False

    @classmethod
    def POW_account_thread_asyc(cls, account):
        valid, frontier = AccountService.validate_PoW(account)
        logger.info('Validating dPoW on account %s as %s' % (account.address, valid))

        if not valid:
            try:
                POWService.enqueue_account(account=account, frontier=frontier)
                logger.info('Generating PoW on start up address %s frontier %s' % (account.address, frontier))
            except Exception as e:
                logger.exception('Account %s dPoW enqueuing error %s' % (account.address, str(e)))

    @classmethod
    def POW_accounts(cls, daemon=True):
        all_accounts = AccountService.get_accounts()

        if not cls._running:
            cls.start(daemon=daemon)

        for account in all_accounts:
            if not cls.in_queue(account):
                cls.thread_pool.apply_async(cls.POW_account_thread_asyc, (account))

        if not daemon:
            cls.thread_pool.close()
            cls.thread_pool.join()

            while not cls.is_empty():
                time.sleep(.1)

            cls.stop()
            cls.thread.join()

    @classmethod
    def ad_hoc_pow(cls, account):
        valid, frontier = AccountService.validate_PoW(account)
        account.POW = cls.get_pow(account=account, hash_value=frontier)
        account.unlock()