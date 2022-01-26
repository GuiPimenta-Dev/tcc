from models.generator import GeneratorModel
from services.connected_generator import ConnectedGeneratorService

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

service = ConnectedGeneratorService(model=GeneratorModel(**args))


class TestConnectedGenerator:
    def test_motor_settings(self):
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
                "voltage": {"min": 232, "max": 720.0, "value": 708.91},
                "power_factor": {"min": 0, "max": 1, "value": 0.8},
            },
        }
        result = service.settings_coords
        assert result == expected_result

    def test_update_load(self):
        expected_result = {
            "coords": {
                "Vt": (32.26, 0.0),
                "Ia": (9.41, -4.838709677419354),
                "Ea": (41.43, 23.521505376344084),
                "RaIa": (0.94, -0.48387096774193544),
                "jXsIa": (12.1, 23.521505376344084),
            },
            "labels": {
                "Vt": "480 ∠ 0°",
                "Ia": "157.43 ∠ -27.22°",
                "Ea": "708.91 ∠ 29.58°",
                "RaIa": "15.74 ∠ -27.22°",
                "jXsIa": "393.57 ∠ 62.78°",
            },
        }
        result = service.update_load(load=140)
        assert result == expected_result

    def test_update_ea(self):
        expected_result = {
            "coords": {
                "Vt": (32.26, 0.0),
                "Ia": (6.33, -1.709005376344086),
                "Ea": (37.16, 15.64516129032258),
                "RaIa": (0.63, -0.17069892473118278),
                "jXsIa": (4.27, 15.815860215053762),
            },
            "labels": {
                "Vt": "480 ∠ 0°",
                "Ia": "97.51 ∠ -15.12°",
                "Ea": "600 ∠ 22.83°",
                "RaIa": "9.75 ∠ -15.12°",
                "jXsIa": "243.78 ∠ 74.88°",
            },
        }

        result = service.update_ea(voltage=600)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {
            "coords": {
                "Vt": (32.26, 0.0),
                "Ia": (8.06, 0.0),
                "Ea": (33.06, 20.161290322580644),
                "RaIa": (0.81, 0.0),
                "jXsIa": (0.0, 20.161290322580644),
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
