from services.motor import MotorService

args = {'Vt': 208, 'Fp': 0.8, 'lagging': False, 'delta': True, 'Xs': 2.5, 'Ra': 0, 'load': 15, 'losses': 2.5}
service = MotorService(params=args)


class TestMotor:

    def test_motor_settings(self):
        expected_result = {
            'coords': {'Vt': (208.0, 0.0), 'Ia': (21.94, 16.45), 'Ea': (249.14, -54.85), 'RaIa': (0.0, 0.0),
                       'jXsIa': (-41.14, 54.85)},
            'labels': {'Vt': '208 ∠ 0°', 'Ia': '27.42 ∠ 36.87°', 'Ea': '255.1 ∠ -12.42°', 'RaIa': '0.0 ∠ 0.0°',
                       'jXsIa': '68.56 ∠ 126.87°'}}
        results = service.settings_coords
        assert results == expected_result

    def test_update_load(self):
        expected_result = {
            'coords': {'Vt': (208.0, 0.0), 'Ia': (39.87, 10.73), 'Ea': (234.82, -99.68), 'RaIa': (0.0, 0.0),
                       'jXsIa': (-41.14, 54.85)},
            'labels': {'Vt': '208 ∠ 0°', 'Ia': '41.29 ∠ 15.06°', 'Ea': '255.1 ∠ -23.0°', 'RaIa': '0.0 ∠ 0.0°',
                       'jXsIa': '68.56 ∠ 126.87°'}}

        result = service.update_load(load=30)
        assert result == expected_result

    def test_update_ea(self):
        expected_result = {
            'coords': {'Vt': (208.0, 0.0), 'Ia': (21.94, 5.12), 'Ea': (220.79, -54.85), 'RaIa': (0.0, 0.0),
                       'jXsIa': (-41.14, 54.85)},
            'labels': {'Vt': '208 ∠ 0°', 'Ia': '22.53 ∠ 13.13°', 'Ea': '227.5 ∠ -13.95°', 'RaIa': '0.0 ∠ 0.0°',
                       'jXsIa': '68.56 ∠ 126.87°'}}

        result = service.update_ea(voltage=227.5)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {'coords': {'Vt': (208.0, 0.0), 'Ia': (27.42, 0.0), 'Ea': (208.0, -68.56), 'RaIa': (0.0, 0.0),
                                      'jXsIa': (0.0, 68.56)},
                           'labels': {'Vt': '208 ∠ 0°', 'Ia': '27.42 ∠ 0.0°', 'Ea': '219.01 ∠ -18.24°',
                                      'RaIa': '0.0 ∠ 0.0°', 'jXsIa': '68.56 ∠ 90.0°'}}

        result = service.update_fp(power_factor=1)
        assert result == expected_result
