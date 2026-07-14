from datetime import date as real_date

import pytest

import app as calendar_app


@pytest.fixture
def client():
    calendar_app.app.config["TESTING"] = True
    return calendar_app.app.test_client()


def test_index_renders_todays_events_for_monday(monkeypatch, client):
    class FakeDate:
        @classmethod
        def today(cls):
            return real_date(2025, 7, 14)

    monkeypatch.setattr(calendar_app, "date", FakeDate)

    response = client.get("/")

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Monday" in page
    assert "July 14, 2025" in page
    assert "Team standup" in page
    assert "Project planning" in page


@pytest.mark.parametrize(
    ("year", "month", "day", "weekday", "expected_title", "expected_time"),
    [
        (2025, 7, 15, "Tuesday", "Design review", "10:30"),
        (2025, 7, 20, "Sunday", "Plan upcoming week", "18:00"),
    ],
)
def test_index_renders_expected_event_for_multiple_days(
    monkeypatch, client, year, month, day, weekday, expected_title, expected_time
):
    class FakeDate:
        @classmethod
        def today(cls):
            return real_date(year, month, day)

    monkeypatch.setattr(calendar_app, "date", FakeDate)

    response = client.get("/")

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert weekday in page
    assert expected_title in page
    assert expected_time in page


def test_index_shows_empty_state_when_no_events_for_day(monkeypatch, client):
    class FakeDate:
        @classmethod
        def today(cls):
            return real_date(2025, 7, 14)

    monkeypatch.setattr(calendar_app, "date", FakeDate)
    monkeypatch.setattr(calendar_app, "EVENTS", {"tuesday": [{"time": "10:00", "title": "Only Tuesday"}]})

    response = client.get("/")

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "No events scheduled for today." in page


def test_index_raises_when_date_provider_fails_in_testing_mode(monkeypatch, client):
    class BrokenDate:
        @classmethod
        def today(cls):
            raise RuntimeError("date lookup failed")

    monkeypatch.setattr(calendar_app, "date", BrokenDate)

    with pytest.raises(RuntimeError, match="date lookup failed"):
        client.get("/")
