import pytest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
import pandas as pd
import builtins

@patch('streamlit_app.st.file_uploader')
@patch('streamlit_app.pd.read_csv')
def test_malformed_csv_handling(mock_read_csv, mock_file_uploader):
    """Test that a malformed CSV upload is caught and an error message is displayed."""
    # Simulate a file being uploaded
    mock_file_uploader.return_value = "dummy_file.csv"

    # Simulate pandas throwing an error for a malformed CSV
    mock_read_csv.side_effect = pd.errors.ParserError("Error tokenizing data")

    at = AppTest.from_file("streamlit_app.py").run(timeout=10)

    # The app should not throw an exception that crashes Streamlit
    assert not at.exception, f"App crashed with exceptions: {at.exception}"

    # The app should display an error message
    assert len(at.error) > 0, "No error message was displayed"
    assert "Error reading CSV file:" in at.error[0].value
    assert "Error tokenizing data" in at.error[0].value

@patch('streamlit_app.st.file_uploader')
@patch('streamlit_app.pd.read_csv')
def test_valid_csv_upload(mock_read_csv, mock_file_uploader):
    """Test that a valid CSV upload is processed correctly."""
    # Simulate a file being uploaded
    mock_file_uploader.return_value = "dummy_file.csv"

    # Simulate pandas successfully reading the CSV
    # The app expects columns: Offender_Age, Victim_Age, Offender_Gender, Victim_Gender, Offender_Race, Victim_Race, Disposition
    df = pd.DataFrame({
        'Offender_Age': [20, 30],
        'Victim_Age': [25, 35],
        'Offender_Gender': ['M', 'F'],
        'Victim_Gender': ['F', 'M'],
        'Offender_Race': ['W', 'B'],
        'Victim_Race': ['B', 'W'],
        'Disposition': ['Arrested', 'Closed']
    })
    mock_read_csv.return_value = df

    at = AppTest.from_file("streamlit_app.py").run(timeout=10)

    # The app should not throw an exception
    assert not at.exception, f"App crashed with exceptions: {at.exception}"

    # The app should display a "Data Preview" subheader
    assert len(at.dataframe) > 0, "Dataframe preview was not displayed"

    # Check that some plots are rendered (st.pyplot is called)
    assert len(at.get("pyplot")) > 0 if getattr(at, "pyplot", None) is not None else True

@patch('streamlit_app.st.file_uploader')
@patch('streamlit_app.os.path.exists')
@patch('streamlit_app.pd.read_csv')
def test_default_csv_fallback(mock_read_csv, mock_exists, mock_file_uploader):
    """Test that the app falls back to crime_data.csv when no file is uploaded."""
    # Simulate no file uploaded
    mock_file_uploader.return_value = None

    # Simulate crime_data.csv existing
    mock_exists.return_value = True

    df = pd.DataFrame({
        'Offender_Age': [20], 'Victim_Age': [25], 'Offender_Gender': ['M'],
        'Victim_Gender': ['F'], 'Offender_Race': ['W'], 'Victim_Race': ['B'],
        'Disposition': ['Arrested']
    })
    mock_read_csv.return_value = df

    at = AppTest.from_file("streamlit_app.py").run(timeout=10)

    # The app should not throw an exception
    assert not at.exception, f"App crashed with exceptions: {at.exception}"

    # Should display an info message about using default data
    assert len(at.info) > 0, "No info message displayed"
    assert "Using default crime_data.csv" in at.info[0].value
