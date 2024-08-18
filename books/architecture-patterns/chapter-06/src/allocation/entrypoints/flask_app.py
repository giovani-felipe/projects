from datetime import datetime

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.allocation import config
from src.allocation.adapters import orm, repository
from src.allocation.domain import model
from src.allocation.service_layer import services

get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_mapping(test_config)

    @app.route("/allocate", methods=["POST"])
    def allocate_endpoint():
        session = get_session()
        repo = repository.SqlAlchemyRepository(session)

        try:
            batchref = services.allocate(request.json['orderid'], request.json['sku'], request.json['qty'], repo, session)
        except (model.OutOfStock, services.InvalidSku) as err:
            return jsonify({'message': str(err)}), 400

        session.commit()
        return jsonify({'batchref': batchref}), 201

    @app.route("/batches", methods=["POST"])
    def add_batch():
        session = get_session()
        repo = repository.SqlAlchemyRepository(session)

        eta = request.json['eta']
        if eta is not None:
            eta = datetime.fromisoformat(eta).date()

        services.add_batch(request.json['ref'], request.json['sku'], request.json['qty'], eta, repo, session)

        return 'OK', 201

    return app


if __name__ == '__main__':
    orm.start_mappers()
    create_app()
