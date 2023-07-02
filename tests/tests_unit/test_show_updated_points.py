import server
from server import app


class TestShowUpdatedPoints:
    client = app.test_client()

    def test_purchase_show_updated_point(self):
        """
        GIVEN an existing club and competition
        WHEN the club has booked some seats
        THEN check the club's points and the
        competition's points have been updated
        and a success message was returned.
        """
        clubs = server.clubs
        competitions = server.competitions
        club = clubs[0]
        competition = competitions[0]
        print(f'\n CLUB POINTS: {int(club["points"])}\n')
        points_before_booking = int(club["points"])
        seats_before_booking = int(competition["numberOfPlaces"])
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
        assert int(competition["numberOfPlaces"]) == seats_before_booking - booked_seats
        assert "Great! Booking complete!" in response.data.decode()

    def test_purchase_not_enough_point(self):
        """
        GIVEN an existing club and competition
        WHEN the club tries to book some seats
        but does not have enough points
        THEN check the club's points and the
        competition's points have not changed
        and a warning message was returned.
        """
        clubs = server.clubs
        competitions = server.competitions
        club = clubs[0]
        competition = competitions[0]
        club["points"] = "10"
        points_before_booking = int(club["points"])
        seats_before_booking = int(competition["numberOfPlaces"])
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
        assert int(competition["numberOfPlaces"]) == seats_before_booking
        assert (
            "You do not have enough points to perform that action"
            in response.data.decode()
        )
