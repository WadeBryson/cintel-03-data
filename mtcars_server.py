""" 
Purpose: Provide reactive output for MT Cars dataset.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

Original Imports 
import pathlib
from shiny import render
import pandas as pd"""
import seaborn as sns

import pathlib
from shiny import render, reactive   # reactive not in original
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
from shinywidgets import render_widget
import plotly.express as px

from util_logger import setup_logger

logger, logname = setup_logger(__name__)


def get_mtcars_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    path_to_data = pathlib.Path(__file__).parent.joinpath("data").joinpath("nuclear.csv")
    original_df = pd.read_csv(path_to_data)

    # Use the len() function to get the number of rows in the DataFrame.
    total_count = len(original_df)

    # New
    reactive_df = reactive.Value()

    @reactive.Effect
    @reactive.event(input.MTCARS_MPG_RANGE, input.MTCARS_MAX_HP, input.Auto_Transmission, input.Manual_Transmission)
    def _():
        df = original_df.copy()

        input_range = input.MTCARS_MPG_RANGE()
        input_min = input_range[0]
        input_max = input_range[1]

        df = df[(df["Date.Year"] >= input_min) & (df["Date.Year"] <= input_max)]

        reactive_df.set(df)

    @output
    @render.table
    def mtcars_table():
        # New
        filtered_df = reactive_df.get()
        return filtered_df
        # return original_df

    @output
    @render.text
    def mtcars_record_count_string():
        # message = f"Showing {total_count} records"
        # logger.debug(f"filter message: {message}")
        # New
        filtered_df = reactive_df.get()
        filtered_count = len(filtered_df)
        message = f"Showing {filtered_count} of {total_count} records"
        return message

    @output
    @render.plot
    def mtcars_plot():
        """
        Use Seaborn to make a quick scatterplot.
        Provide a pandas DataFrame and the names of the columns to plot.
        Learn more at https://stackabuse.com/seaborn-scatter-plot-tutorial-and-examples/
        """
        # New
        df = reactive_df.get()
        plt = sns.scatterplot(
            data=df,    # Changed original_df to df
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
