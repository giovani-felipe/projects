import json
import logging
from dataclasses import asdict

import redis

from src.allocation import config
from src.allocation.adapters import orm
from src.allocation.domain import commands
from src.allocation.domain.events import Event
from src.allocation.service_layer.message_bus.message_bus import MessageBus
from src.allocation.service_layer.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())


def publish(channel, event: Event):
    logger.debug('publishing: channel=%s, event=%s', channel, event)
    r.publish(channel, json.dumps(asdict(event)))


def main():
    logger.info("Starting")
    orm.start_mappers()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('change_batch_quantity')

    for m in pubsub.listen():
        logger.info("Starting")
        handle_change_batch_quantity(m)


def handle_change_batch_quantity(message):
    logger.debug('handling %s', message)
    message_bus = MessageBus()
    data = json.loads(message['data'])
    cmd = commands.ChangeBatchQuantity(ref=data['batchref'], qty=data['qty'])
    message_bus.handle(cmd, uow=SqlAlchemyUnitOfWork())


if __name__ == '__main__':
    main()
