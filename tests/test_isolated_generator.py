from services.isolated_generator import IsolatedGeneratorService
from models.generator import GeneratorModel

args = {
    "Vt": 480,
    "Il": 120,
    "VtN": 600,
    "Fp": 0.8,
    "Xs": 2.5,
    "Ra": 0.1,
    "losses": 70,
    "lead_lag": "lag",
    "delta_star": "star",
}

service = IsolatedGeneratorService(model=GeneratorModel(**args))


class TestIsolatedGenerator:
    def test_generator_settings(self):
        expected_result = {
            "coords": {
                "Vt": (32.26, 0.0),
                "Ia": (6.45, -4.838709677419354),
                "Ea": (45.0, 15.64516129032258),
                "RaIa": (0.65, -0.48387096774193544),
                "jXsIa": (12.1, 16.129032258064516),
            },
            "labels": {
                "Vt": "480 ∠ 0°",
                "Ia": "120 ∠ -36.87°",
                "Ea": "708.91 ∠ 19.17°",
                "RaIa": "12.0 ∠ -36.87°",
                "jXsIa": "300.0 ∠ 53.13°",
            },
            "sliders": {
                "load": {"min": 0, "max": 180.0, "value": 120},
                "voltage": {"min": 1, "max": 720.0, "value": 708.91},
                "power_factor": {"min": 0, "max": 1, "value": 0.8},
            },
        }

        results = service.settings_coords
        assert results == expected_result

    def test_update_load(self):
        expected_result = {
            "coords": {
                "Vt": (29.72, 0.5803993864190106),
                "Ia": (7.74, -5.803993864190105),
                "Ea": (45.0, 19.34664621396702),
                "RaIa": (0.77, -0.5803993864190106),
                "jXsIa": (14.51, 19.34664621396702),
            },
            "labels": {
                "Vt": "430.16 ∠ 1.12°",
                "Ia": "140 ∠ -36.87°",
                "Ea": "708.91 ∠ 23.26°",
                "RaIa": "14.0 ∠ -36.87°",
                "jXsIa": "350.0 ∠ 53.13°",
            },
        }

        result = service.update_load(load=140)
        assert result == expected_result

    def test_update_ea(self):
        expected_result = {
            'coords': {'Vt': (32.26, 0.0), 'Ia': (6.45, -4.838684131958277), 'Ea': (45.0, 15.645384745459022),
                       'RaIa': (0.65, -0.48356236106856915), 'jXsIa': (12.1, 16.12894710652759)},
            'labels': {'Vt': '316.2 ∠ 0°', 'Ia': '79.05 ∠ -36.87°', 'Ea': '467 ∠ 19.17°', 'RaIa': '7.91 ∠ -36.87°',
                       'jXsIa': '197.63 ∠ 53.13°'}}

        result = service.update_ea(voltage=467)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {
            "coords": {
                "Vt": (43.9, 0.0),
                "Ia": (10.98, 0.0),
                "Ea": (45.0, 27.4390243902439),
                "RaIa": (1.1, 0.0),
                "jXsIa": (0.0, 27.4390243902439),
            },
            "labels": {
                "Vt": "480 ∠ 0°",
                "Ia": "120 ∠ 0.0°",
                "Ea": "576.25 ∠ 31.37°",
                "RaIa": "12.0 ∠ 0.0°",
                "jXsIa": "300.0 ∠ 90.0°",
            },
        }

        result = service.update_fp(power_factor=1)
        assert result == expected_result
