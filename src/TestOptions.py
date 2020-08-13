import unittest
from reb_options import REBOptions
from figures import Rectangle
from station import Station


class TestOptions(unittest.TestCase):
    def setUp(self):
        self.rect = Rectangle(
            36,
            25,
            -46,
            -35
        )

        self.station = Station(
            "NVAR",
            38.43,
            -118.3,
            []
        )

        self.options = REBOptions(
            self.rect,
            "../tests",
            [
                self.station
            ]
        )

        self.options.process_directories()

        self.events = self.options.get_events()

        self.first = self.events[0]
        self.second = self.events[1]

    def test_rect_in(self):
        self.assertTrue(
            self.rect.check_inside(
                30,
                -40
            )
        )

    def test_rect_out(self):
        self.assertFalse(
            self.rect.check_inside(
                100,
                100
            )
        )

    def test_events_length(self):
        self.assertEqual(
            len(self.events),
            3
        )

    def test_first_event_latitude(self):
        self.assertEqual(
            self.first.latitude,
            31.8863
        )

    def test_first_event_longtitude(self):
        self.assertEqual(
            self.first.longtitude,
            -40.6214
        )

    def test_first_event_number(self):
        self.assertEqual(
            self.first.event,
            "15761185"
        )

    def test_first_event_date(self):
        self.assertEqual(
            self.first.date,
            "2018/05/03"
        )

    def test_second_event_latitude(self):
        self.assertEqual(
            self.second.latitude,
            35.5392
        )

    def test_second_event_longtitude(self):
        self.assertEqual(
            self.second.longtitude,
            -35.7236 
        )

    def test_second_event_number(self):
        self.assertEqual(
            self.second.event,
            "1641063"
        )

    def test_second_event_date(self):
        self.assertEqual(
            self.second.date,
            "2003/04/02"
        )


if __name__ == "__main__":
    unittest.main()
