from server import app, clubs, competitions, club_booked_seats


class TestUpToTwelveSeats:
    client = app.test_client()

    def setup_method(self):
        self.club = clubs[0]

    def test_purchase_more_than_twelve_seats(self):
        club = self.club
        competition = competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 13,
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) >= 0
        assert "You cannot book more than 12 seats at once." in response.data.decode()

    def test_purchase_up_to_twelve_seats(self):
        club = self.club
        competition = competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 12,
            },
        )
        assert response.status_code == 200
        assert int(club["points"]) >= 0
        assert "Great! Booking complete!" in response.data.decode()

    def test_purchase_a_13th_seat(self):
        club = self.club
        competition = competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 1,
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) >= 0
        assert (
            "You cannot book more than 12 seats for each competition."
            in response.data.decode()
        )
