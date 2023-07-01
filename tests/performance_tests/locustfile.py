from locust import HttpUser, task, between
from server import loadClubs, loadCompetitions


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    club = loadClubs()[0]
    competition = loadCompetitions()[0]

    @task
    def home(self):
        self.client.get("/", name="index")

    @task
    def clubs_board(self):
        self.client.get("/clubs_board", name="Clubs Board")

    @task
    def login(self):
        self.client.post(
            "/showSummary",
            data={"email": self.club["email"]},
            name="login, showSummary",
        )

    @task
    def booking_page(self):
        self.client.get(
            f'/book/{self.competition["name"]}/{self.club["name"]}', name="booking page"
        )

    @task
    def purchase_page(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club["name"],
                "competition": self.competition["name"],
                "places": 0,
            },
            name="purchase seats",
        )
