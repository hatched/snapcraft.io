import responses
from flask_testing import TestCase
from webapp.app import create_app


class GetGitHubBadgeTest(TestCase):
    render_templates = False

    snap_payload = {
        "snap-id": "id",
        "name": "snapName",
        "default-track": "test",
        "snap": {
            "title": "Snap Title",
            "summary": "This is a summary",
            "description": "this is a description",
            "media": [],
            "license": "license",
            "prices": 0,
            "publisher": {
                "display-name": "Toto",
                "username": "toto",
                "validation": True,
            },
            "categories": [{"name": "test"}],
        },
        "channel-map": [
            {
                "channel": {
                    "architecture": "amd64",
                    "name": "stable",
                    "risk": "stable",
                    "track": "latest",
                },
                "created-at": "2018-09-18T14:45:28.064633+00:00",
                "version": "1.0",
                "confinement": "conf",
                "download": {"size": 100000},
            },
            {
                "channel": {
                    "architecture": "amd64",
                    "name": "stable",
                    "risk": "stable",
                    "track": "test",
                },
                "created-at": "2018-09-18T14:45:28.064633+00:00",
                "version": "1.0",
                "confinement": "conf",
                "download": {"size": 100000},
            },
        ],
    }

    def setUp(self):
        self.snap_name = "toto"
        self.api_url = "".join(
            [
                "https://api.snapcraft.io/v2/",
                "snaps/info/",
                self.snap_name,
                "?fields=title,summary,description,license,contact,website,",
                "publisher,prices,media,download,version,created-at,"
                "confinement,categories",
            ]
        )
        self.endpoint_url = "/" + self.snap_name + "/badge.svg"

    def create_app(self):
        app = create_app(testing=True)
        app.secret_key = "secret_key"
        app.config["WTF_CSRF_METHODS"] = []

        return app

    @responses.activate
    def test_api_404(self):
        payload = {"error-list": []}
        responses.add(
            responses.Response(
                method="GET", url=self.api_url, json=payload, status=404
            )
        )

        response = self.client.get(self.endpoint_url)

        assert len(responses.calls) == 1
        called = responses.calls[0]
        assert called.request.url == self.api_url

        assert response.status_code == 404

    @responses.activate
    def test_api_500(self):
        payload = {"error-list": []}
        responses.add(
            responses.Response(
                method="GET", url=self.api_url, json=payload, status=500
            )
        )

        response = self.client.get(self.endpoint_url)

        assert len(responses.calls) == 1
        called = responses.calls[0]
        assert called.request.url == self.api_url

        assert response.status_code == 502

    @responses.activate
    def test_api_500_no_answer(self):
        responses.add(
            responses.Response(method="GET", url=self.api_url, status=500)
        )

        response = self.client.get(self.endpoint_url)

        assert len(responses.calls) == 1
        called = responses.calls[0]
        assert called.request.url == self.api_url

        assert response.status_code == 502

    @responses.activate
    def test_get_badge(self):
        payload = self.snap_payload

        responses.add(
            responses.Response(
                method="GET", url=self.api_url, json=payload, status=200
            )
        )

        response = self.client.get(self.endpoint_url)

        self.assertEqual(response.status_code, 200)
        # self.assert_context("snap_title", "Snap Title")
