from services.connected_generator import ConnectedGeneratorService

args = {'Vt': 480, 'Il': 1200, 'Fp': 0.8, 'Xs': 0.1, 'Ra': 0.015, 'losses': 70, 'lagging': True, 'delta': False}
service = ConnectedGeneratorService(params=args)


class TestConnectedGenerator:

    def test_motor_settings(self):
        expected_result = {
            'coords': {'Vt': (480.0, 0.0), 'Ia': (960.0, -720.0), 'Ea': (566.4, 85.2), 'RaIa': (14.4, -10.8),
                       'jXsIa': (72.0, 96.0)},
            'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ -36.87°', 'Ea': '572.77 ∠ 8.55°', 'RaIa': '18.0 ∠ -36.87°',
                       'jXsIa': '120.0 ∠ 53.13°'}}
        results = service.settings_coords
        assert results == expected_result

    def test_update_load(self):
        expected_result = {
            'coords': {'Vt': (288.0, 0.0), 'Ia': (1600.0, -1200.0), 'Ea': (432.0, 142.0), 'RaIa': (24.0, -18.0),
                       'jXsIa': (120.0, 160.0)},
            'labels': {'Vt': '288.0 ∠ 0°', 'Ia': '2000 ∠ -36.87°', 'Ea': '454.74 ∠ 18.2°', 'RaIa': '30.0 ∠ -36.87°',
                       'jXsIa': '200.0 ∠ 53.13°'}}

        result = service.update_load(load=2000)
        assert result == expected_result

    def test_update_vt(self):
        expected_result = {
            'coords': {'Vt': (750.0, 0.0), 'Ia': (614.4, -460.8), 'Ea': (805.3, 54.53), 'RaIa': (9.22, -6.91),
                       'jXsIa': (46.08, 61.44)},
            'labels': {'Vt': '750 ∠ 0°', 'Ia': '768.0 ∠ -36.87°', 'Ea': '807.14 ∠ 3.87°', 'RaIa': '11.52 ∠ -36.87°',
                       'jXsIa': '76.8 ∠ 53.13°'}}

        result = service.update_vt(voltage=750)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {
            'coords': {'Vt': (480.0, 0.0), 'Ia': (1200.0, 0.0), 'Ea': (498.0, 120.0), 'RaIa': (18.0, 0.0),
                       'jXsIa': (0.0, 120.0)},
            'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ 0.0°', 'Ea': '512.25 ∠ 13.55°', 'RaIa': '18.0 ∠ 0.0°',
                       'jXsIa': '120.0 ∠ 90.0°'}}
        result = service.update_fp(power_factor=1)
        assert result == expected_result
