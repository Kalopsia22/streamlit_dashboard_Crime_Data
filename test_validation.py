import sys
from unittest.mock import MagicMock

# Mock streamlit and pandas before they are imported by utils
sys.modules['streamlit'] = MagicMock()
sys.modules['pandas'] = MagicMock()

import unittest
from unittest.mock import patch
import pandas as pd
from utils import validate_columns

class TestValidation(unittest.TestCase):
    @patch('utils.st')
    def test_validate_columns_valid(self, mock_st):
        # Create a mock dataframe with all required columns
        df = MagicMock()
        df.columns = [
            'Offender_Age', 'Victim_Age', 'Offender_Gender', 'Victim_Gender',
            'Offender_Race', 'Victim_Race', 'Disposition'
        ]

        # Call validate_columns
        validate_columns(df)

        # Verify st.error and st.stop are not called
        mock_st.error.assert_not_called()
        mock_st.stop.assert_not_called()

    @patch('utils.st')
    def test_validate_columns_invalid(self, mock_st):
        # Create a mock dataframe missing some required columns
        df = MagicMock()
        df.columns = [
            'Offender_Age', 'Victim_Age'
        ]

        # Call validate_columns
        validate_columns(df)

        # Verify st.error and st.stop are called
        mock_st.error.assert_called_once()
        self.assertTrue(mock_st.error.call_args[0][0].startswith("Missing required columns in CSV:"))
        mock_st.stop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
