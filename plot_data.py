from obspy import read
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import json
import calendar


def make_plot_dictionary():
    """
    Makes dictionary with available plots in directories.

    plot_dictionary[year][month][day][doy] is the corresponding day of the year for day and month of year,
    plot_dictionary[year][month][day][stations] are the stations that have plots for day and month of year.

    :return: plot dictionary
    """
    plot_dict = {}
    for year in [1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977]:
        plot_dict[year] = {}

        for month in range(1, 13):
            plot_dict[year][month] = {}

        # check if each station has a plot for a day
        for station in ["s11", "s12", "s14", "s15", "s16"]:
            directory = os.path.join(os.getcwd(), "plots", station, str(year))
            available_days = []
            for (dirpath, dirnames, filenames) in os.walk(directory):
                available_days.extend(dirnames)
                break
            available_days = set([int(day) for day in available_days])

            if calendar.isleap(year):
                day_range = range(1, 367)
            else:
                day_range = range(1, 366)
            # days of year
            for day in day_range:
                # days of year converted to dates
                date = pd.to_datetime(year*1000 + day, format="%Y%j")
                day_month = int(date.day)
                month = int(date.month)

                # first time visiting day of month, init
                if day_month not in plot_dict[year][month]:
                    plot_dict[year][month][day_month] = {}
                    plot_dict[year][month][day_month]["doy"] = "%03d" % day
                    plot_dict[year][month][day_month]["stations"] = []

                # station has a plot for day
                if day in available_days:
                    plot_dict[year][month][day_month]["stations"].append(station)

        # output
        file_path_out = os.path.join(os.getcwd(), "plots", "plot_dict.json")
        with open(file_path_out, "w") as file_out:
            file_out.write(json.dumps(plot_dict, indent=4))


def get_saved_stations(return_num=False):
    """
    Gets available stations from saved directories.

    :param return_num: if True returns station name as number instead of string (e.g. 11 instead of "s11")
    :return: station name list (empty if data doesn't exist)
    """
    directory = os.path.join(os.getcwd(), "data")
    if not os.path.isdir(directory):
        return []

    stations = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        stations.extend(dirnames)
        break

    try:
        stations.remove("nakamura")
    except ValueError:
        pass

    if return_num:
        stations = [int(station[1:]) for station in stations]

    return stations


def get_saved_years(station, return_num=False):
    """
    Gets available data years for a station from saved directories.

    :param station: station name
    :param return_num: if True returns year as number instead of string
    :return: years list (empty if station name is invalid or data doesn't exist)
    """
    # add "s" in front of station number
    station = str(station)
    if not station.startswith("s"):
        station = "s" + station

    directory = os.path.join(os.getcwd(), "data", station)
    if not os.path.isdir(directory):
        return []

    years = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        years.extend(dirnames)
        break

    if return_num:
        years = [int(year) for year in years]

    return years


def get_saved_days(station, year, return_num=False):
    """
    Gets available data days for a year of a station from saved directories.

    :param station: station name
    :param year: year
    :param return_num: if True returns day as number instead of 3-character string (e.g. 1 instead of "001")
    :return: days of the year list (empty if station name or year are invalid or data doesn't exist)
    """
    # add "s" in front of station number
    station = str(station)
    if not station.startswith("s"):
        station = "s" + station

    directory = os.path.join(os.getcwd(), "data", station, str(year))
    if not os.path.isdir(directory):
        return []

    days = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        days.extend(dirnames)
        break

    if return_num:
        days = [int(day) for day in days]

    return days


def sensor_plot(ax=None, fontsize=15, title='', tr=None):
    """
    Adds plot with PSE data to axis.

    :param ax: axis
    :param fontsize: plot title fontsize
    :param title: plot title
    :param tr: trace
    """
    ax.locator_params(nbins=3)
    ax.set_xlabel('Time', fontsize=fontsize)
    ax.set_ylabel('DU', fontsize=fontsize)
    ax.set_yticks(np.linspace(min(tr.data), max(tr.data), 5))
    ax.set_title(title, fontsize=20, fontweight="bold", pad=10)
    ax.plot(tr.times("matplotlib"), tr.data, "b-")
    ax.xaxis_date()


def plot_data(stations=None, years=None, days=None, display=False):
    """
    Plots PSE data and calculates max deviation from average values for every plot.

    :param stations: station name or station name list (only valid station names used), if None plot for all saved
                     stations
    :param years: year or year list, if None plot  for all available years
    :param days: day or day list, if None plot for all available days
    :param display: display plots if True
    """
    saved_stations = get_saved_stations(return_num=True)
    if stations is None:
        valid_stations = ["s" + str(station) for station in saved_stations]  # all available stations
    else:
        if not isinstance(stations, list):
            stations = [stations]
        # only valid stations
        valid_stations = [str(station) for station in stations if int(str(station).lstrip("s")) in saved_stations]

    for index_station, station in enumerate(valid_stations):
        saved_years = get_saved_years(station, return_num=False)
        if years is None:
            valid_years = saved_years  # all available years
        else:
            if not isinstance(years, list):
                years = [years]
            # only valid years
            valid_years = [str(year) for year in years if str(year) in saved_years]

        for index_year, year in enumerate(valid_years):
            saved_days = get_saved_days(station, year, return_num=True)
            if days is None:
                valid_days = ["%03d" % day for day in saved_days]  # all available days
            else:
                if not isinstance(days, list):
                    days = [days]
                # only valid days
                valid_days = ["%03d" % int(day) for day in days if int(day) in saved_days]

            for index_day, day in enumerate(valid_days):
                # add "s" in front of station number
                if not station.startswith("s"):
                    station_name = "s" + station
                else:
                    station_name = station

                # iterate over files in directory to read data
                daily_trace = {}
                daily_max = {}
                directory_in = os.path.join(os.getcwd(), "data", station_name, year, day)
                for filename in os.listdir(directory_in):
                    file = os.path.join(directory_in, filename)

                    st = read(file)
                    tr = st[0]
                    tr.data = tr.data.astype(np.float64)

                    avg = np.average(tr.data[tr.data != -1])
                    max_dev = np.max(np.abs(tr.data - avg))
                    tr.data[tr.data == -1] = np.nan

                    sensor = filename[10:13]
                    daily_trace[sensor] = tr  # save trace of this day
                    daily_max[sensor] = max_dev

                # plot data from files
                with plt.style.context("seaborn-darkgrid"):
                    fig, ((ax1), (ax2), (ax3)) = plt.subplots(nrows=3, ncols=1)
                    fig.set_figwidth(15)
                    fig.set_figheight(15)
                    if "mh1" in daily_max and "mh1" in daily_trace:
                        sensor_plot(ax=ax1, title='MH1 (Mid-Period Sensor)     ' +
                                                  '[Max Deviation Value: ' + str(daily_max['mh1']) + ']',
                                    tr=daily_trace['mh1'])
                    if "mh2" in daily_max and "mh2" in daily_trace:
                        sensor_plot(ax=ax2, title='MH2 (Mid-Period Sensor)     ' +
                                                  '[Max Deviation Value: ' + str(daily_max['mh2']) + ']',
                                    tr=daily_trace['mh2'])
                    if "mhz" in daily_max and "mhz" in daily_trace:
                        sensor_plot(ax=ax3, title='MHZ (Mid-Period Sensor)     ' +
                                                  '[Max Deviation Value: ' + str(daily_max['mhz']) + ']',
                                    tr=daily_trace['mhz'])
                    try:
                        fig.tight_layout(pad=1.5)
                        fig.subplots_adjust(hspace=0.3)

                        if display:
                            fig.show()

                        # output plot
                        file_out = "{station}_{year}_{day}_mh_plot.png".format(station=station_name, year=year, day=day)
                        directory_out = os.path.join(os.getcwd(), "plots", station_name, year, day)
                        if not os.path.isdir(directory_out):
                            os.makedirs(directory_out)
                        file_path_out = os.path.join(directory_out, file_out)
                        fig.savefig(file_path_out)
                        plt.close(fig)

                        print("Saved",
                              station,
                              "({station}/{stations})".format(station=index_station + 1, stations=len(valid_stations)),
                              year, "({year}/{years})".format(year=index_year + 1, years=len(valid_years)),
                              day, "({day}/{days})".format(day=index_day + 1, days=len(valid_days)))

                        # output max deviation
                        file_out = "{station}_{year}_{day}_mh_dev.json".format(station=station_name, year=year, day=day)
                        file_path_out = os.path.join(directory_out, file_out)
                        with open(file_path_out, "w") as file_out:
                            file_out.write(json.dumps(daily_max, indent=4))
                    except ValueError:
                        print("ERROR",
                              station,
                              "({station}/{stations})".format(station=index_station + 1, stations=len(valid_stations)),
                              year, "({year}/{years})".format(year=index_year + 1, years=len(valid_years)),
                              day, "({day}/{days})".format(day=index_day + 1, days=len(valid_days)))

                        continue


if __name__ == "__main__":
    plot_data("s11")
    plot_data("s12")
    plot_data("s14")
    plot_data("s15")
    plot_data("s16")

    make_plot_dictionary()