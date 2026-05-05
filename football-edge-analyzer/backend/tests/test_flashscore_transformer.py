from app.services.flashscore_transformer import normalize_flashscore_csv


def test_normalize_flashscore_csv_maps_basic_columns():
    csv_content = """match_id,date,status,home_name,away_name,home_goals,away_goals\nabc-123,2026-05-01,FT,Team A,Team B,2,1\n"""

    matches = normalize_flashscore_csv(csv_content)

    assert len(matches) == 1
    assert matches[0].external_id == "abc-123"
    assert matches[0].home.name == "Team A"
    assert matches[0].away.name == "Team B"
    assert matches[0].result.home == 2
    assert matches[0].result.away == 1


def test_normalize_flashscore_csv_falls_back_to_unknown_team_names():
    csv_content = """match_id,home_goals,away_goals\nxyz-789,0,0\n"""

    matches = normalize_flashscore_csv(csv_content)

    assert len(matches) == 1
    assert matches[0].home.name == "Unknown Home"
    assert matches[0].away.name == "Unknown Away"
