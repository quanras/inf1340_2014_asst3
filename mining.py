#!/usr/bin/env python3

""" Docstring """

__author__ = 'Evan Moir'
__email__ = "evan.moir@utoronto.ca"

__copyright__ = "2014 Evan Moir"
__license__ = "CC0 Creative Commons Public Domain"

__status__ = "Final Submission"

# imports one per line
import json
from datetime import date
from operator import itemgetter

# Initialize the dictionary to hold monthly averages.
monthly_averages = {}

def read_stock_data(stock_name, stock_file_name):
    """
    :param stock_name: The stock's ticker symbol
    :param stock_file_name: the name of the file containing the JSON stock data.
    :return: a dictionary containing the monthly average stock prices {year/month: average, year/month: average, ...}

    The monthly average is calculated using the following formula:

        avg = sum(Vi * Ci) / sum(Vi)

        where:
            Vi is the volume of stocks traded on the given day
            Ci is the close price of the stock on the given day

    This function makes the following assumptions about the stock data file:
        1. The file is complete and well-structured, i.e. every daily entry has all of the required values,
            formatted correctly and containing no missing characters that break the data's structure.
        2. The values in the file are sensible based on context, e.g. there are no negative prices or trade volumes.
        2. All of the daily stock entries for a given month are consecutive in the file.

    """

    # Use the provided function to create a stock_data list from the given JSON file.
    stock_data = read_json_from_file(stock_file_name)

    # Initialize the numerator and denominator variables that will hold the running totals for calculating
    # the average price of a given month.
    numerator = 0
    denominator = 0

    # Get the month and year of the first entry in the stock data.
    last_entry_month = stock_data[0]['Date'][5:7]
    last_entry_year = stock_data[0]['Date'][0:4]

    last_entry_date =

    for daily_entry in stock_data:

        # If this entry is in the same month as the last entry, add to running average for that month.
        # For the first entry, this will be true because of how the date was initialized.
        if daily_entry['Date'][5:7] == last_entry_month and daily_entry['Date'][8:10] == last_entry_year:
            numerator += float(daily_entry['Close']) * int(daily_entry['Volume'])
            denominator += int(daily_entry['Volume'])

        # Alternatively, if this day's entry is from a different month,
        # calculate the average for the month that just "ended" and insert it into monthly_averages.
        else:
            # Check to ensure total volume for the month (denominator) is not 0. If it is, use 0 as the monthly average.
            if not denominator == 0:
                monthly_average = numerator / denominator
            else:
                monthly_average = 0

            # Add calculated monthly average to monthly_averages dictionary
            date_string = str(last_entry_year) + '/' + str(last_entry_month)
            monthly_averages[date_string] = monthly_average

            # Restart numerator and denominator counting for new month.
            numerator = float(daily_entry['Close']) * int(daily_entry['Volume'])
            denominator = int(daily_entry['Volume'])

        # Re-set last date info to current entry's date for use in next iteration.
        last_entry_month = daily_entry['Date'][5:7]
        last_entry_year = daily_entry['Date'][0:4]

    return monthly_averages


def six_best_months():
    """
    :param monthly_averages: a dictionary of months and their associated average stock prices for a given stock
    :return: a list of the 6 months with the highest average stock prices. Each item in the list is a tuple:
        [year/month, average_price]
    """
    # Create a reverse sorted list out of monthly_averages, sorting by the dictionary values (highest -> lowest).
    highest_monthly_averages = sorted(monthly_averages, key=itemgetter(2), reverse=True)

    # Return a list containing the first six sorted items.
    return highest_monthly_averages[0:6]


def six_worst_months():
    """
    :param monthly_averages: a dictionary of months and their associated average stock prices for a given stock
    :return: a list of the 6 months with the lowest average stock prices. Each item in the list is a list
    containing two items: [year/month, average_price]
    """
    # Create sorted list of lists out of monthly_averages, sorting by the dictionary values (lowest -> highest).
    lowest_monthly_averages = sorted(monthly_averages, key=itemgetter(2))

    # Return a list containing the first sorted six items.
    return lowest_monthly_averages[0:6]


# This function was provided, so I did not create a docstring for it.
def read_json_from_file(file_name):
    with open(file_name) as file_handle:
        file_contents = file_handle.read()

    return json.loads(file_contents)
