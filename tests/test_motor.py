from services.motor import MotorService
from models.motor import MotorModel

args = {
    "Vt": 208,
    "VtN": 308,
    "Fp": 0.8,
    "lead_lag": "lead",
    "delta_star": "delta",
    "Xs": 2.5,
    "Ra": 0,
    "kw_load": 15,
    "losses": 2.5,
}
service = MotorService(model=MotorModel(**args))


class TestMotor:
    def test_motor_settings(self):
        expected_result = {
            "coords": {
                "Vt": (37.57, 0.0),
                "Ia": (3.96, 2.9712708834866675),
                "Ea": (45.0, -9.907246684452506),
                "RaIa": (0.0, 0.0),
                "jXsIa": (-7.43, 9.907246684452506),
            },
            "labels": {
                "Vt": "208 ∠ 0°",
                "Ia": "27.42 ∠ 36.87°",
                "Ea": "255.1 ∠ -12.42°",
                "RaIa": "0.0 ∠ 0.0°",
                "jXsIa": "68.56 ∠ 126.87°",
            },
            "sliders": {
                "load": {"min": 0, "max": 35, "value": 15},
                "voltage": {"min": 55, "max": 369.6, "value": 255.1},
                "power_factor": {"min": 0, "max": 1, "value": 0.8},
            },
        }
        results = service.settings_coords
        assert results == expected_result

    def test_update_load(self):
        expected_result = {
            "coords": {
                "Vt": (37.57, 0.0),
                "Ia": (7.2, 1.9380994881344649),
                "Ea": (42.41, -18.00463718334049),
                "RaIa": (0.0, 0.0),
                "jXsIa": (-4.84, 18.00463718334049),
            },
            "labels": {
                "Vt": "208 ∠ 0°",
                "Ia": "41.29 ∠ 15.06°",
                "Ea": "255.1 ∠ -23.0°",
                "RaIa": "0.0 ∠ 0.0°",
                "jXsIa": "103.22 ∠ 105.06°",
            },
        }

        result = service.update_load(load=30)
        assert result == expected_result

    def test_update_ea(self):
        expected_result = {
            "coords": {
                "Vt": (37.57, 0.0),
                "Ia": (3.96, 0.9247967734621118),
                "Ea": (39.88, -9.907246684452506),
                "RaIa": (0.0, 0.0),
                "jXsIa": (-2.31, 9.907246684452506),
            },
            "labels": {
                "Vt": "208 ∠ 0°",
                "Ia": "22.53 ∠ 13.13°",
                "Ea": "227.5 ∠ -13.95°",
                "RaIa": "0.0 ∠ 0.0°",
                "jXsIa": "56.32 ∠ 103.13°",
            },
        }

        result = service.update_ea(voltage=227.5)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {
            "coords": {
                "Vt": (37.57, 0.0),
                "Ia": (4.95, 0.0),
                "Ea": (37.57, -12.383606794641091),
                "RaIa": (0.0, 0.0),
                "jXsIa": (0.0, 12.383606794641091),
            },
            "labels": {
                "Vt": "208 ∠ 0°",
                "Ia": "27.42 ∠ 0.0°",
                "Ea": "219.01 ∠ -18.24°",
                "RaIa": "0.0 ∠ 0.0°",
                "jXsIa": "68.56 ∠ 90.0°",
            },
        }

        result = service.update_fp(power_factor=1)
        assert result == expected_result
