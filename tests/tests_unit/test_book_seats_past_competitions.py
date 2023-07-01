from server import app, check_competition_date


class TestSeatsPastCompetition:
    competitions_test = [
        {
            "name": "Spring Festival",
            "date": "2028-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
    ]

    def test_past_competition(self):
        competition = self.competitions_test[1]
        competitions_over, competitions_ongoing = check_competition_date(
            self.competitions_test
        )

        assert competition in competitions_over

    def test_coming_competition(self):
        competition = self.competitions_test[0]
        competitions_over, competitions_ongoing = check_competition_date(
            self.competitions_test
        )

        assert competition in competitions_ongoing
