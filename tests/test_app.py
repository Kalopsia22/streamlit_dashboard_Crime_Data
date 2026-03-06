import pytest
from streamlit.testing.v1 import AppTest

def test_default_dataset_loading():
    """Test that the app loads the default dataset when no file is uploaded."""
    at = AppTest.from_file("streamlit_app.py").run(timeout=10)

    # The title should be present
    assert at.title[0].value == "Crime Data Analysis Dashboard"

    # Default info message should be shown
    assert at.info[0].value == "Using default crime_data.csv"

    # Check if a dataframe is rendered (meaning data was loaded)
    assert len(at.dataframe) > 0

    # Ensure charts are rendered
    assert len(at.subheader) >= 7
    assert "Age Distribution" in [sh.value for sh in at.subheader]
