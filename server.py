import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


def check_competition_date(competitions):
    competitions_over = []
    competitions_ongoing = []
    current_date = datetime.now().replace(microsecond=0)
    for competition in competitions:
        competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        if current_date < competition_date:
            competitions_ongoing.append(competition)
        else:
            competitions_over.append(competition)
    return competitions_over, competitions_ongoing


all_booked_seats = []
for competition in competitions:
    for club in clubs:
        all_booked_seats.append(
            {
                "competition": competition["name"],
                "club": club["name"],
                "booked_seats": 0,
            }
        )


def club_booked_seats(competition, club, all_booked_seats, placesRequired):
    for booked_seats in all_booked_seats:
        if (
            booked_seats["competition"] == competition["name"]
            and booked_seats["club"] == club["name"]
        ):
            if booked_seats["booked_seats"] + placesRequired <= 12:
                booked_seats["booked_seats"] += placesRequired
                break
            else:
                raise ValueError(
                    "Every club is limited to 12 seats for each competition."
                )

    return all_booked_seats


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Please enter your email.")
        print("\nThe provided email is not valid.\n")
        return redirect(url_for("index"))
    competitions_over, competitions_ongoing = check_competition_date(competitions)
    return render_template(
        "welcome.html",
        club=club,
        clubs=clubs,
        competitions=competitions,
        competitions_over=competitions_over,
        competitions_ongoing=competitions_ongoing,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    availablePlaces = int(competition["numberOfPlaces"])
    club_points = int(club["points"])
    print(f"\nCLUB'S POINT: {club_points}")

    placesRequired = abs(int(request.form["places"]))

    competitions_over, competitions_ongoing = check_competition_date(competitions)

    if placesRequired > 12:
        flash("You cannot book more than 12 seats at once.")

    elif placesRequired == 0:
        flash("It's technically hard to order nothing...")

    elif placesRequired > availablePlaces:
        flash("You are ordering more places than there are available!")

    else:
        try:
            club_booked_seats(competition, club, all_booked_seats, placesRequired)
            if club_points - placesRequired >= 0:
                competition["numberOfPlaces"] = (
                    int(competition["numberOfPlaces"]) - placesRequired
                )
                club_points -= placesRequired
                club["points"] = str(club_points)
                flash("Great! Booking complete!")

            else:
                flash("You do not have enough points to perform that action")
        except ValueError:
            flash("You cannot book more than 12 seats for each competition.")

    return render_template(
        "welcome.html",
        club=club,
        clubs=clubs,
        competitions=competitions,
        competitions_over=competitions_over,
        competitions_ongoing=competitions_ongoing,
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
