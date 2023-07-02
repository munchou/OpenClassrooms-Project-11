import server
from server import app


class TestUpToTwelveSeats:
    client = app.test_client()

    def test_purchase_more_than_twelve_seats(self):
        """
        GIVEN an existing club and competition
        WHEN the club tries to book more than 12 seats
        THEN check the club's points and the
        competition's points have not changed and a
        warning message was returned.
        """
        clubs = server.clubs
        competitions = server.competitions
        # all_booked_seats = server.all_booked_seats
        club = clubs[0]
        competition = competitions[0]
        points_before_booking = int(club["points"])
        seats_before_booking = int(competition["numberOfPlaces"])
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": 13,
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) == points_before_booking
        assert int(competition["numberOfPlaces"]) == seats_before_booking
        assert "You cannot book more than 12 seats at once." in response.data.decode()

    def test_purchase_up_to_twelve_seats(self):
        """
        GIVEN an existing club and competition
        WHEN the club books 12 seats (= max allowed)
        THEN check the club's points and the
        competition's points have been updated and a
        success message was returned.
        """
        clubs = server.clubs
        competitions = server.competitions
        # all_booked_seats = server.all_booked_seats
        club = clubs[0]
        competition = competitions[0]
        points_before_booking = int(club["points"])
        seats_before_booking = int(competition["numberOfPlaces"])
        booked_seats = 12
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": booked_seats,
            },
        )
        # print(f"\nBOOKED SEATS: {booked_seats}\n")
        assert response.status_code == 200
        assert int(club["points"]) == points_before_booking - booked_seats
        assert competition["numberOfPlaces"] == seats_before_booking - booked_seats
        assert "Great! Booking complete!" in response.data.decode()

    def test_purchase_a_13th_seat(self):
        """
        GIVEN an existing club and competition
        WHEN the club books 12 seats (= max allowed)
        THEN check the club's points and the
        competition's points have been updated and a
        success message was returned.
        """
        clubs = server.clubs
        competitions = server.competitions
        all_booked_seats = server.all_booked_seats
        club = clubs[0]
        competition = competitions[0]
        all_booked_seats[0]["booked_seats"] = 12
        booked_seats = 1
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": booked_seats,
            },
        )

        assert response.status_code == 200
        assert (
            "You cannot book more than 12 seats for each competition."
            in response.data.decode()
        )
