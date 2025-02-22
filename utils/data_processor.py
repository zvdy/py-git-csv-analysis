import pandas as pd
import streamlit as st

class DataProcessor:
    @staticmethod
    def filter_dataframe(df, filters):
        """Apply filters to dataframe."""
        filtered_df = df.copy()

        for column, value in filters.items():
            if value is not None:  # Check for None to handle boolean False values
                if pd.api.types.is_bool_dtype(df[column]):
                    if value != "Both":  # Only filter if not showing both values
                        filtered_df = filtered_df[filtered_df[column] == (value == "True")]
                elif pd.api.types.is_numeric_dtype(df[column]):
                    try:
                        min_val, max_val = value
                        filtered_df = filtered_df[
                            (filtered_df[column] >= min_val) & 
                            (filtered_df[column] <= max_val)
                        ]
                    except:
                        st.warning(f"Invalid filter value for {column}")
                else:
                    filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(value, case=False)]

        return filtered_df

    @staticmethod
    def get_column_filters(df):
        """Create appropriate filters based on column types."""
        filters = {}
        for column in df.columns:
            if pd.api.types.is_bool_dtype(df[column]):
                # Use radio buttons for boolean columns
                filters[column] = st.radio(
                    f"Filter {column}",
                    options=["Both", "True", "False"],
                    horizontal=True,
                    key=f"bool_{column}"
                )
            elif pd.api.types.is_numeric_dtype(df[column]):
                min_val = float(df[column].min())
                max_val = float(df[column].max())

                # Handle case where min and max are equal
                if min_val == max_val:
                    max_val += 1  # Add a buffer of 1
                    st.info(f"Column '{column}' has constant value {min_val}")

                filters[column] = st.slider(
                    f"Filter {column}",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    key=f"slider_{column}"
                )
            else:
                filters[column] = st.text_input(
                    f"Filter {column}",
                    key=f"text_{column}"
                )
        return filters

    @staticmethod
    def download_csv(df, filename):
        """Convert dataframe to CSV for download."""
        return df.to_csv(index=False).encode('utf-8')