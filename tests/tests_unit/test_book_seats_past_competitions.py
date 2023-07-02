import server
from server import check_competition_date


class TestSeatsPastCompetition:
    def test_past_competition(self):
        """
        GIVEN an existing competition
        WHEN the competition is being loaded
        THEN check the competition date is prior
        to the current date.
        """
        competitions = server.competitions
        competitions_over, competitions_ongoing = check_competition_date(competitions)

        assert competitions_over == [competitions[1]]

    def test_coming_competition(self):
        """
        GIVEN an existing competition
        WHEN the competition is being loaded
        THEN check the current date is prior
        to the competition date.
        """
        competitions = server.competitions
        competitions_over, competitions_ongoing = check_competition_date(competitions)

        assert competitions_ongoing == [competitions[0]]
