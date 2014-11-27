#!/usr/bin/env python3

""" Docstring """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
from mining import *

# Define Test Functions


def test_goog():
    read_stock_data("GOOG", "data/GOOG.json")
    assert six_best_months() == [('2007/12', 693.76), ('2007/11', 676.55), ('2007/10', 637.38), ('2008/01', 599.42),
                                 ('2008/05', 576.29), ('2008/06', 555.34)]
    assert six_worst_months() == [('2004/09', 116.38), ('2004/10', 164.52), ('2004/11', 177.09), ('2004/12', 181.01),
                                  ('2005/03', 181.18), ('2005/01', 192.96)]


def test_goog_2005():
    read_stock_data("GOOG2005", "data/GOOG-2005.json.json")
    assert six_best_months() == [('2005/12', 418.74), ('2005/11', 398.73), ('2005/10', 323.93), ('2005/09', 306.33),
                                 ('2005/07', 300.15), ('2005/06', 287.95)]
    assert six_worst_months() == [('2005/03', 181.18), ('2005/02', 195.25), ('2005/04', 203.99), ('2005/05', 245.1),
                                  ('2005/08', 286.55), ('2005/06', 287.95)]


def test_two_stocks_highest_std_dev():

    assert two_stocks_highest_std_dev("GOOG", "data/GOOG.json", "GOOG", "data/GOOG.json") == 0


if __name__ == '__main__':
    read_stock_data("GOOG", "data/GOOG.json")
    print(six_best_months())
    print(six_worst_months())
    test_goog()
    # read_stock_data("GOOG2005", "data/GOOG-2005.json")
    # big_months = sorted(all_monthly_averages.keys())
    # for month in big_months:
    #     print(month + ' : ' + str(all_monthly_averages[month]) + '/n')