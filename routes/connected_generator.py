from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse
from models.generator import GeneratorModel

from app import logger
from services.connected_generator import ConnectedGeneratorService
from utils.constants import CONNECTED_GENERATOR_ROUTE_PREFIX

bp = Blueprint('connected_generator', __name__, url_prefix=CONNECTED_GENERATOR_ROUTE_PREFIX)
nms = Namespace('Connected Generator')

connected_generator_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = connected_generator_parser.copy()
voltage_parser = connected_generator_parser.copy()
power_factor_parser = connected_generator_parser.copy()

connected_generator_parser.add_argument('Vt', required=False, type=float, location='json', default=480)
connected_generator_parser.add_argument('VtN', required=False, type=float, location='json', default=600)
connected_generator_parser.add_argument('Il', required=False, type=float, location='json', default=120)
connected_generator_parser.add_argument('Fp', required=False, type=float, location='json', default=0.8)
connected_generator_parser.add_argument('Xs', required=False, type=float, location='json', default=2.5)
connected_generator_parser.add_argument('Ra', required=False, type=float, location='json', default=0)
connected_generator_parser.add_argument('losses', required=False, type=float, location='json', default=70)
connected_generator_parser.add_argument('lead_lag', required=False, type=str, location='json', choices=['lead', 'lag'],
                                        default='lag')
connected_generator_parser.add_argument('delta_star', required=False, type=str, location='json',
                                        choices=['delta', 'star'], default='star')

load_parser.add_argument('load', required=False, type=float, location='json', default=30)

voltage_parser.add_argument('Ea', required=False, type=float, location='json', default=227.5)

power_factor_parser.add_argument('Fp', required=False, type=float, location='json', default=1)


class BaseConnectedGenerator(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_connected_generator(self, model: GeneratorModel):
        BaseConnectedGenerator.connected_generator = ConnectedGeneratorService(model=model)


@nms.route('')
class Settings(BaseConnectedGenerator):
    @nms.expect(connected_generator_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def post(self):
        args = connected_generator_parser.parse_args()
        try:
            self.create_connected_generator(model=GeneratorModel(**args))
            return self.connected_generator.settings_coords

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/load')
class Load(BaseConnectedGenerator):
    @nms.expect(load_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        load = load_parser.parse_args()['load']
        try:
            return self.connected_generator.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/voltage')
class Voltage(BaseConnectedGenerator):
    @nms.expect(voltage_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        vt = voltage_parser.parse_args()['Ea']
        try:
            return self.connected_generator.update_ea(voltage=vt)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/power_factor')
class PowerFactor(BaseConnectedGenerator):
    @nms.expect(power_factor_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        fp = power_factor_parser.parse_args()['Fp']
        try:
            return self.connected_generator.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
