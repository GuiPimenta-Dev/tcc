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
                "voltage": {"min": 363, "max": 720.0, "value": 708.91},
                "power_factor": {"min": 0, "max": 1, "value": 0.8},
            },
        }
        result = service.settings_coords
        assert result == expected_result

    def test_update_load(self):
        expected_result = {
            "coords": {
                "Vt": (35.04, 0.0),
                "Ia": (10.22, -5.255559148449189),
                "Ea": (45.0, 25.547856971628),
                "RaIa": (1.02, -0.5255559148449189),
                "jXsIa": (13.14, 25.547856971628),
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
                "Vt": (39.28, 0.0),
                "Ia": (7.93, -1.971325865919396),
                "Ea": (45.0, 19.63961012123931),
                "RaIa": (0.79, -0.1972144183007781),
                "jXsIa": (4.93, 19.83682453954009),
            },
            "labels": {
                "Vt": "480 ∠ 0°",
                "Ia": "99.91 ∠ -13.95°",
                "Ea": "600 ∠ 23.58°",
                "RaIa": "9.99 ∠ -13.95°",
                "jXsIa": "249.77 ∠ 76.05°",
            },
        }

        result = service.update_ea(voltage=600)
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
