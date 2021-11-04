from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse

from app import logger
from utils.constants import GENERATOR_ROUTE_PREFIX

bp = Blueprint('generator', __name__, url_prefix=GENERATOR_ROUTE_PREFIX)
nms = Namespace('Generator')
base_parser = reqparse.RequestParser(bundle_errors=True)


@nms.route('/generator')
class Motor(Resource):
    @nms.expect()
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def post(self):
        try:
            return 'generator'

        except Exception as e:
            logger.info(str(e))
            raise
