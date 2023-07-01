from server import app, clubs, competitions


class TestShowUpdatedPoints:
    client = app.test_client()

    def test_purchase_show_updated_point(self):
        club = clubs[2]
        competition = competitions[0]
        points_before_booking = int(club["points"])
        booked_seats = 3
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": booked_seats,
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) == points_before_booking - booked_seats
        assert "Great! Booking complete!" in response.data.decode()

    def test_purchase_not_enough_point(self):
        club = clubs[2]
        competition = competitions[1]
        points_before_booking = int(club["points"])
        booked_seats = 10
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": booked_seats,
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) == points_before_booking
        assert (
            "You do not have enough points to perform that action"
            in response.data.decode()
        )
