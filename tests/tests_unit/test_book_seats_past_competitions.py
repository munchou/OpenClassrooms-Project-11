from server import check_competition_date
from datetime import datetime, timedelta


class TestSeatsPastCompetition:
    future_date = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    past_date = (datetime.now() + timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S")

    competitions_test = [
        {
            "name": "Spring Festival",
            "date": future_date,
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": past_date,
            "numberOfPlaces": "13",
        },
    ]

    def test_past_competition(self):
        competitions_over, competitions_ongoing = check_competition_date(
            self.competitions_test
        )

        assert competitions_over == [self.competitions_test[1]]

    def test_coming_competition(self):
        competitions_over, competitions_ongoing = check_competition_date(
            self.competitions_test
        )

        assert competitions_ongoing == [self.competitions_test[0]]
