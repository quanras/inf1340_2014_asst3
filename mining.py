#!/usr/bin/env python3

""" Docstring """

__author__ = 'Evan Moir'
__email__ = "evan.moir@utoronto.ca"

__copyright__ = "2014 Evan Moir"
__license__ = "CC0 Creative Commons Public Domain"

__status__ = "Final Submission"

# imports one per line
import json
from operator import itemgetter
from statistics import stdev

# Initialize the dictionary to hold monthly averages.
all_monthly_averages = []


def read_stock_data(stock_name, stock_file_name):
    """
    :param stock_name: the stock's ticker symbol
    :param stock_file_name: the name of the file containing the JSON stock data.
    :return: a list containing tuples of the monthly average stock prices [year/month: average, ...]

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

    for daily_entry in stock_data:

        # If this entry is in the same month as the last entry, add to running average for that month.
        # For the first entry, this will be true because of how the date was initialized.
        if daily_entry['Date'][5:7] == last_entry_month and daily_entry['Date'][0:4] == last_entry_year:
            numerator += float(daily_entry['Close']) * int(daily_entry['Volume'])
            denominator += int(daily_entry['Volume'])

        # Alternatively, if this day's entry is from a different month than the last entry,
        # calculate the average for the month that just "ended" and insert it into monthly_averages.
        else:
            # Check to ensure total volume for the month (denominator) is not 0. If it is, use 0 as the monthly average.
            if not denominator == 0:
                monthly_average = numerator / denominator
            else:
                monthly_average = 0

            # Add calculated monthly average (rounded to two digits) to monthly_averages dictionary
            date_string = str(last_entry_year) + '/' + str(last_entry_month)
            all_monthly_averages.append((date_string, round(monthly_average, 2)))

            # Restart numerator and denominator counting for new month.
            numerator = float(daily_entry['Close']) * int(daily_entry['Volume'])
            denominator = int(daily_entry['Volume'])

        # Re-set last date info to current entry's date for use in next iteration.
        last_entry_month = daily_entry['Date'][5:7]
        last_entry_year = daily_entry['Date'][0:4]

    return all_monthly_averages


def six_best_months():
    """
    :return: a list of the 6 months with the highest average stock prices, using the current value of the global
    variable all_monthly_averages as its data source.
    Each item in the list is a tuple: (year/month, average_price)
    """
    # Create a reverse sorted list out of monthly_averages, sorting by the dictionary values (highest -> lowest).
    highest_monthly_averages = sorted(all_monthly_averages, key=itemgetter(1), reverse=True)

    # Return a list containing the first six sorted items.
    return highest_monthly_averages[0:6]


def six_worst_months():
    """
    :return: a list of the 6 months with the lowest average stock prices, using the current value of the global
    variable all_monthly_averages as its data source.
    Each item in the list is a tuple: (year/month, average_price)
    """
    # Create sorted list of lists out of monthly_averages, sorting by the dictionary values (lowest -> highest).
    lowest_monthly_averages = sorted(all_monthly_averages, key=itemgetter(1))

    # Return a list containing the first sorted six items.
    return lowest_monthly_averages[0:6]


# This function was provided, so I didn't create a docstring for it.
def read_json_from_file(file_name):
    with open(file_name) as file_handle:
        file_contents = file_handle.read()

    return json.loads(file_contents)


def two_stocks_highest_std_dev(first_stock_name, first_stock_file, second_stock_name, second_stock_file):
    """
    Determine which of two stocks has the highest standard deviation of monthly averages in the given data sets.
    Uses the stdev function from the statistics package. Note that this ignores whether the data used for the two stocks
    covers same time period

    :param first_stock_name: string, the ticker symbol of the first stock
    :param first_stock_file: JSON file containing the first stock's daily stock entries
    :param second_stock_name: string, the ticker symbol of the second stock
    :param second_stock_file:JSON file containing the second stock's daily stock entries
    :return: the ticker symbol of the stock with the higher standard deviation of monthly averages (to 2 decimal places)
        # or 0, if either:
            - the two stocks have the same standard deviation of monthly averages (to 2 decimal places), or
            - one of the passed stock lengths is less than 2 (this would make calculating stdev impossible).
    #
    """

    first_stock_monthly_averages = read_stock_data(first_stock_name, first_stock_file)
    second_stock_monthly_averages = read_stock_data(second_stock_name, second_stock_file)

    if len(first_stock_monthly_averages) < 2 or len(second_stock_monthly_averages) < 2:
        return 0

    # Create a list for each stock with only the numbers - no month identifier strings.
    first_stock_averages_only = []
    second_stock_averages_only = []

    for monthly_average in first_stock_monthly_averages:
        first_stock_averages_only.append(monthly_average[1])

    for monthly_average in second_stock_monthly_averages:
        second_stock_averages_only.append(monthly_average[1])

    #Calculate stdev values and return appropriate value
    first_stock_stdev = round(stdev(first_stock_averages_only), 2)
    second_stock_stdev = round(stdev(second_stock_averages_only), 2)

    if first_stock_stdev == second_stock_stdev:
        return 0
    elif first_stock_stdev > second_stock_stdev:
        return first_stock_name
    else:
        return second_stock_name