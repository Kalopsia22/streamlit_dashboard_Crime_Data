import streamlit as st

def validate_columns(df):
    """
    Validates that all required columns are present in the DataFrame.
    If not, it calls st.error and st.stop.
    """
    required_columns = [
        'Offender_Age', 'Victim_Age', 'Offender_Gender', 'Victim_Gender',
        'Offender_Race', 'Victim_Race', 'Disposition'
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Missing required columns in CSV: {', '.join(missing_columns)}")
        st.stop()
