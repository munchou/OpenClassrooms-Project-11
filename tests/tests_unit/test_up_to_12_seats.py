import server
from server import app


class TestUpToTwelveSeats:
    client = app.test_client()

    clubs = [
        {"name": "Club 10", "email": "club1@zupatester.com", "points": "13"},
    ]

    competitions = [
        {
            "name": "Competition 10",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
    ]

    booked_seats = [
        {
            "club": "Club 10",
            "competition": "Competition 10",
            "booked_seats": 0,
        },
    ]

    def setup_method(self):
        server.clubs = self.clubs
        server.competitions = self.competitions
        server.all_booked_seats = self.booked_seats

    def test_purchase_more_than_twelve_seats(self):
        club = self.clubs[0]
        competition = self.competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 13,
            },
        )

        print(f"\nBOOKED SEATS: {self.booked_seats}\n")
        assert response.status_code == 200
        assert int(club["points"]) == 13
        assert "You cannot book more than 12 seats at once." in response.data.decode()

    def test_purchase_up_to_twelve_seats(self):
        club = self.clubs[0]
        competition = self.competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 12,
            },
        )
        print(f"\nBOOKED SEATS: {self.booked_seats}\n")
        assert response.status_code == 200
        assert int(club["points"]) == 1
        assert competition["numberOfPlaces"] == 13
        assert "Great! Booking complete!" in response.data.decode()

    def test_purchase_a_13th_seat(self):
        club = self.clubs[0]
        competition = self.competitions[0]
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 1,
            },
        )

        print(f"\nBOOKED SEATS: {self.booked_seats}\n")
        assert response.status_code == 200
        assert (
            "You cannot book more than 12 seats for each competition."
            in response.data.decode()
        )
