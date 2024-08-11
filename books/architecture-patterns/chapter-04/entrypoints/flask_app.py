from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from adapters import orm, repository
from domain import model
from service_layer import services

get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_mapping(test_config)

    @app.route("/allocate", methods=["POST"])
    def allocate_endpoint():
        session = get_session()
        repo = repository.SqlAlchemyRepository(session)
        line = model.OrderLine(request.json['orderid'], request.json['sku'], request.json['qty'])

        try:
            batchref = services.allocate(line, repo, session)
        except (model.OutOfStock, services.InvalidSku) as err:
            return jsonify({'message': str(err)}), 400

        session.commit()
        return jsonify({'batchref': batchref}), 201

    return app


if __name__ == '__main__':
    orm.start_mappers()
    create_app()
