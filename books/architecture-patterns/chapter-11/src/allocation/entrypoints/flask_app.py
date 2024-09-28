from datetime import datetime

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.allocation import config
from src.allocation.adapters import orm
from src.allocation.domain import commands, events
from src.allocation.service_layer import services
from src.allocation.service_layer.error import InvalidSku
from src.allocation.service_layer.message_bus.message_bus import MessageBus
from src.allocation.service_layer.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork

get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_mapping(test_config)

    @app.route("/allocate", methods=["POST"])
    def allocate_endpoint():
        try:
            event = commands.Allocate(request.json['orderid'], request.json['sku'], request.json['qty'])
            message_bus = MessageBus()
            results = message_bus.handle(message=event, uow=SqlAlchemyUnitOfWork())
            batchref = results.pop(0)
        except services.InvalidSku as err:
            return jsonify({'message': str(err)}), 400

        return jsonify({'batchref': batchref}), 201

    @app.route("/batches", methods=["POST"])
    def add_batch():
        try:
            uow = SqlAlchemyUnitOfWork()
            message_bus = MessageBus()

            eta = request.json['eta']
            if eta is not None:
                eta = datetime.fromisoformat(eta).date()

            cmd = commands.CreateBatch(request.json['ref'], request.json['sku'], request.json['qty'], eta)
            results = message_bus.handle(cmd, uow)
            batchref = results.pop(0)
        except InvalidSku as err:
            return {'message': str(err)}, 400
        return {'batchref': batchref}, 201

    return app


if __name__ == '__main__':
    orm.start_mappers()
    create_app()
