from server import app, clubs, competitions


class TestAllowedPoints:
    client = app.test_client()

    club_test = [
        {
            "name": "Club",
            "email": "test@club.com",
            "points": "13",
        }
    ]
    competition_test = [
        {
            "name": "Competition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        }
    ]

    def setup_method(self):
        self.club = clubs[1]

    def test_purchase_with_enough_point(self):
        club = self.club
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
        club = self.club
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
        club = self.club
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
        club = self.club
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
