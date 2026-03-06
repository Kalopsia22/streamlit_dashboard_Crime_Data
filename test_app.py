import os
import pytest
from streamlit.testing.v1 import AppTest

def test_missing_data_warning(tmp_path):
    """
    Test that the app displays a warning message when crime_data.csv is missing
    and no file has been uploaded.
    """
    # Temporarily rename crime_data.csv to simulate it being missing
    original_file = "crime_data.csv"
    temp_file = "crime_data.csv.bak"

    file_renamed = False
    if os.path.exists(original_file):
        os.rename(original_file, temp_file)
        file_renamed = True

    try:
        # Initialize and run the Streamlit AppTest
        at = AppTest.from_file("streamlit_app.py")
        at.run()

        # Check if the warning message is displayed
        assert not at.exception

        # Verify the warning text
        warnings = [warning.value for warning in at.warning]
        assert "Please upload a CSV file to proceed." in warnings

    finally:
        # Restore the original file
        if file_renamed and os.path.exists(temp_file):
            os.rename(temp_file, original_file)

def test_existing_data():
    """
    Test that the app runs successfully when crime_data.csv exists.
    """
    if os.path.exists("crime_data.csv"):
        at = AppTest.from_file("streamlit_app.py")
        at.run(timeout=30)

        assert not at.exception
        # Ensure that the default message is shown
        infos = [info.value for info in at.info]
        assert "Using default crime_data.csv" in infos

        # No warning should be displayed about uploading a CSV
        warnings = [warning.value for warning in at.warning]
        assert "Please upload a CSV file to proceed." not in warnings
