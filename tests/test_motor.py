from services.motor import MotorService
from models.motor import MotorModel

args = {'Vt': 208, 'VtN': 308, 'Fp': 0.8, 'lead_lag': 'lead', 'delta_star': 'delta', 'Xs': 2.5, 'Ra': 0, 'kw_load': 15,
        'losses': 2.5}
model = MotorModel(**args)
service = MotorService(model=model)


class TestMotor:

    def test_motor_settings(self):
        expected_result = {
            'coords': {'Vt': (37.57, 0.0), 'Ia': (3.96, 2.9712708834866675), 'Ea': (45.0, -9.907246684452506),
                       'RaIa': (0.0, 0.0), 'jXsIa': (-7.43, 9.907246684452506)},
            'labels': {'Vt': '208 ∠ 0°', 'Ia': '27.42 ∠ 36.87°', 'Ea': '255.1 ∠ -12.42°', 'RaIa': '0.0 ∠ 0.0°',
                       'jXsIa': '68.56 ∠ 126.87°'}, 'sliders': {'load': {'min': 0, 'max': 82, 'value': 15},
                                                                'voltage': {'min': 55, 'max': 369.6, 'value': 255.1},
                                                                'power_factor': {'min': 0, 'max': 1, 'value': 0.8}}}

        results = service.settings_coords
        assert results == expected_result

    def test_update_load(self):
        expected_result = {
            'coords': {'Vt': (39.86, 0.0), 'Ia': (7.64, 2.0562465461406885), 'Ea': (45.0, -19.102204633672304),
                       'RaIa': (0.0, 0.0), 'jXsIa': (-5.14, 19.102204633672304)},
            'labels': {'Vt': '208 ∠ 0°', 'Ia': '41.29 ∠ 15.06°', 'Ea': '255.1 ∠ -23.0°', 'RaIa': '0.0 ∠ 0.0°',
                       'jXsIa': '103.22 ∠ 105.06°'}}

        result = service.update_load(load=30)
        assert result == expected_result

    def test_update_ea(self):
        expected_result = {
            'coords': {'Vt': (42.39, 0.0), 'Ia': (4.47, 1.0435282029757045), 'Ea': (45.0, -11.179203502581522),
                       'RaIa': (0.0, 0.0), 'jXsIa': (-2.61, 11.179203502581522)},
            'labels': {'Vt': '208 ∠ 0°', 'Ia': '22.53 ∠ 13.13°', 'Ea': '227.5 ∠ -13.95°', 'RaIa': '0.0 ∠ 0.0°',
                       'jXsIa': '56.32 ∠ 103.13°'}}

        result = service.update_ea(voltage=227.5)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {
            'coords': {'Vt': (45.0, 0.0), 'Ia': (5.93, 0.0), 'Ea': (45.0, -14.832692307692307), 'RaIa': (0.0, 0.0),
                       'jXsIa': (0.0, 14.832692307692307)},
            'labels': {'Vt': '208 ∠ 0°', 'Ia': '27.42 ∠ 0.0°', 'Ea': '219.01 ∠ -18.24°', 'RaIa': '0.0 ∠ 0.0°',
                       'jXsIa': '68.56 ∠ 90.0°'}}

        result = service.update_fp(power_factor=1)
        assert result == expected_result
