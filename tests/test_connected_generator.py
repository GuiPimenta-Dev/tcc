from services.connected_generator import ConnectedGeneratorService

args = {'Vt': 480, 'Il': 1200, 'Fp': 0.8, 'Xs': 0.1, 'Ra': 0.015, 'losses': 70, 'lagging': True, 'delta': False}
service = ConnectedGeneratorService(params=args)


class TestConnectedGenerator:

    def test_motor_settings(self):
        expected_result = {
            'coords': {'Vt': (22.5, 0.0), 'Ia': (45.0, -33.74999999999999), 'Ea': (26.55, 3.993749999999999),
                       'RaIa': (0.67, -0.5062499999999999), 'jXsIa': (3.37, 4.499999999999998)},
            'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ -36.87°', 'Ea': '572.77 ∠ 8.55°', 'RaIa': '18.0 ∠ -36.87°',
                       'jXsIa': '120.0 ∠ 53.13°'}}

        result = service.settings_coords
        assert result == expected_result

    def test_update_load(self):
        expected_result = {'coords': {'Vt': (8.1, 0.0), 'Ia': (45.0, -33.75), 'Ea': (12.15, 3.9937499999999995),
                                      'RaIa': (0.68, -0.50625), 'jXsIa': (3.37, 4.5)},
                           'labels': {'Vt': '288.0 ∠ 0°', 'Ia': '2000 ∠ -36.87°', 'Ea': '454.74 ∠ 18.2°',
                                      'RaIa': '30.0 ∠ -36.87°', 'jXsIa': '200.0 ∠ 53.13°'}}

        result = service.update_load(load=2000)
        assert result == expected_result

    def test_update_vt(self):
        expected_result = {
            'coords': {'Vt': (41.91, 0.0), 'Ia': (34.33, -25.749538058055673), 'Ea': (45.0, 3.047140430351076),
                       'RaIa': (0.51, -0.38613131072301365), 'jXsIa': (2.57, 3.433271741074089)},
            'labels': {'Vt': '750 ∠ 0°', 'Ia': '768.0 ∠ -36.87°', 'Ea': '807.14 ∠ 3.87°', 'RaIa': '11.52 ∠ -36.87°',
                       'jXsIa': '76.8 ∠ 53.13°'}}

        result = service.update_vt(voltage=750)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {'coords': {'Vt': (18.0, 0.0), 'Ia': (45.0, 0.0), 'Ea': (18.68, 4.5), 'RaIa': (0.67, 0.0),
                                      'jXsIa': (0.0, 4.5)},
                           'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ 0.0°', 'Ea': '512.25 ∠ 13.55°',
                                      'RaIa': '18.0 ∠ 0.0°', 'jXsIa': '120.0 ∠ 90.0°'}}
        result = service.update_fp(power_factor=1)
        assert result == expected_result
