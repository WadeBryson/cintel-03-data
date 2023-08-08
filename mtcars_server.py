""" 
Purpose: Provide reactive output for MT Cars dataset.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

"""
import pathlib
from shiny import render
import pandas as pd
import seaborn as sns

from util_logger import setup_logger

logger, logname = setup_logger(__name__)


def get_mtcars_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    path_to_data = pathlib.Path(__file__).parent.joinpath("data").joinpath("nuclear.csv")
    original_df = pd.read_csv(path_to_data)

    # Use the len() function to get the number of rows in the DataFrame.
    total_count = len(original_df)

    @output
    @render.table
    def mtcars_table():
        return original_df

    @output
    @render.text
    def mtcars_record_count_string():
        message = f"Showing {total_count} records"
        logger.debug(f"filter message: {message}")
        return message

    @output
    @render.plot
    def mtcars_plot():
        """
        Use Seaborn to make a quick scatterplot.
        Provide a pandas DataFrame and the names of the columns to plot.
        Learn more at https://stackabuse.com/seaborn-scatter-plot-tutorial-and-examples/
        """
        plt = sns.scatterplot(
            data=original_df,
            x="Date.Year",
            y="Data.Yeild.Upper",
        )
        return plt

    # return a list of function names for use in reactive outputs
    return [
        mtcars_table,
        mtcars_record_count_string,
        mtcars_plot,
    ]
