import server
from server import app, clubs, competitions


class TestShowUpdatedPoints:
    client = app.test_client()

    clubs = [
        {"name": "Club 255", "email": "club255@zupatester.com", "points": "13"},
    ]

    competitions = [
        {
            "name": "Competition 255",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
    ]

    def setup_method(self):
        server.clubs = self.clubs
        server.competitions = self.competitions

    def test_purchase_show_updated_point(self):
        club = self.clubs[0]
        competition = self.competitions[0]
        print(f'\n CLUB POINTS 1 {club["points"]}')
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
        club = self.clubs[0]
        competition = self.competitions[0]
        points_before_booking = int(club["points"])
        booked_seats = 11
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
