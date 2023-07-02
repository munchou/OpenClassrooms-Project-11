import server
from server import app


class TestAllowedPoints:
    client = app.test_client()

    def test_purchase_with_enough_point(self):
        """
        GIVEN an existing club and competition
        WHEN the club books seats with enough points (<= 12)
        THEN check the booking was successful and a
        confirmation message was displayed
        """
        clubs = server.clubs
        competitions = server.competitions
        club = clubs[0]
        competition = competitions[0]

        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 3,
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) >= 0
        assert "Great! Booking complete!" in response.data.decode()

    def test_purchase_not_enough_points(self):
        """
        GIVEN an existing club and competition
        WHEN the club books seats with not enough points
        THEN check the booking was cancelled and a
        warning was displayed
        """
        clubs = server.clubs
        competitions = server.competitions
        club = clubs[1]
        competition = competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 8,
            },
        )
        assert response.status_code == 200
        assert int(club["points"]) >= 0
        assert (
            "You do not have enough points to perform that action"
            in response.data.decode()
        )

    def test_purchase_OK_with_negative_input(self):
        """
        GIVEN an existing club and competition
        WHEN the club books seats with enough points (<= 12)
        but entered a minus before the points (ex: "-5")
        THEN check the booking was successful and a
        confirmation message was displayed, which means
        the negative input was converted its a positive
        counterpart
        """
        clubs = server.clubs
        competitions = server.competitions
        club = clubs[0]
        competition = competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": -1,
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) >= 0
        assert "Great! Booking complete!" in response.data.decode()

    def test_purchase_with_null_input(self):
        """
        GIVEN an existing club and competition
        WHEN the club books 0 seat
        THEN check the booking was cancelled and a
        warning was displayed
        """
        clubs = server.clubs
        competitions = server.competitions
        club = clubs[0]
        competition = competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 0,
            },
        )
        assert response.status_code == 200
        assert int(club["points"]) >= 0
        assert "technically hard to order nothing" in response.data.decode()
