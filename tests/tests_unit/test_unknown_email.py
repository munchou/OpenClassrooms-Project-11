from server import app


class TestLoginEmail:
    client = app.test_client()

    def test_existing_email(self):
        """
        GIVEN an existing (= registered) email
        WHEN an email is entered in the input box
        THEN check the email is valid
        """

        result = self.client.post("/showSummary", data=dict(email="john@simplylift.co"))
        output = result.status_code
        expected = 200
        assert output == expected

    def test_no_email(self):
        """
        GIVEN no email (= wrong email)
        WHEN nothing is entered in the input box
        THEN check there is nothing hence the redirection happens
        """
        result = self.client.post("/showSummary", data=dict(email=""))
        # assert result.status_code == 500
        # Returns 500 if not TRY/EXCEPT fix
        output = result.status_code
        expected = 302
        # where 302 = <WrapperTestResponse streamed [302 FOUND]>.status_code => redirect
        assert output == expected

    def test_unknown_email(self):
        """
        GIVEN a wrong email (= wrong input, non existing email)
        WHEN a wrong email is entered in the input box
        THEN check the email is wrong hence the redirection happens
        """
        result = self.client.post(
            "/showSummary", data=dict(email="labanana@testmail.com")
        )
        # assert result.status_code == 500
        # Returns 500 if not TRY/EXCEPT fix
        output = result.status_code
        expected = 302
        assert output == expected
