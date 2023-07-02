import server
from server import app


class TestIntegration:
    client = app.test_client()

    def test_integration(self):
        """Integration test that checks the log in,
        the booking of several seats, and that the available
        points as well as the available seats were properly
        updated and well displayed."""
        clubs = server.clubs
        competitions = server.competitions
        booked_seats = 9
        club = clubs[0]
        competition = competitions[0]
        # log in:
        self.client.post("/showSummary", data={"email": clubs[0]["email"]})

        # book some seats:
        points_before_booking = int(club["points"])
        seats_before_booking = int(competition["numberOfPlaces"])
        self.client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": booked_seats,
            },
        )

        # go to the Clubs Board:
        response = self.client.get("/clubs_board")
        print(response.data.decode())
        # assert:
        assert response.status_code == 200
        assert int(club["points"]) == points_before_booking - booked_seats
        assert int(competition["numberOfPlaces"]) == seats_before_booking - booked_seats
        assert f"<th>{club['name']}</th>" in response.data.decode()
        assert (
            f'<th style="text-align: center">{points_before_booking - booked_seats}</th>'
            in response.data.decode()
        )

    """ Extra test that were not done before"""

    def test_book_page(self):
        """
        GIVEN an existing club and competition
        WHEN the club accesses the booking page of the target competition
        THEN check the booking page exists
        """
        clubs = server.clubs
        competitions = server.competitions
        print(f"\nJOURNAL: {competitions[0]} / {clubs[0]}\n")
        response = self.client.get(
            f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
        )
        assert response.status_code == 200

    def test_logout(self):
        """
        GIVEN an existing user
        WHEN the user log outs
        THEN check the URI exists and the redirection happens
        """
        response = self.client.get("/logout")
        assert response.status_code == 302
