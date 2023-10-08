import matplotlib.pyplot as plt
from obspy import read
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError
import bs4 as bs
import os
import time


def fetch_stations(return_num=False):
    """
    Fetches available stations for PSE data.

    :param return_num: if True returns station name as number instead of string (e.g. 11 instead of "s11")
    :return: station name list
    """
    url = "https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/data/xa/continuous_waveform/"
    source = urlopen(url).read()

    soup = bs.BeautifulSoup(source, "html.parser")

    stations = []
    for a in soup.find_all("a", href=True):
        href_text = a.getText()
        if href_text.find("Parent") == -1:
            if return_num:
                href_text = int(href_text[1:])
            stations.append(href_text)

    return stations


def fetch_years(station, return_num=False):
    """
    Fetches available years of PSE data for a station.

    :param station: station name
    :param return_num: if True returns year as number instead of string
    :return: years list (empty if station name is invalid)
    """
    # add "s" in front of station number
    station = str(station)
    if not station.startswith("s"):
        station = "s" + station

    try:
        url = "https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/data/xa/continuous_waveform/" \
              "{station}/".format(station=station)
        source = urlopen(url).read()
    except HTTPError:
        return []

    soup = bs.BeautifulSoup(source, "html.parser")

    years = []
    for a in soup.find_all("a", href=True):
        href_text = a.getText()
        if href_text.find("Parent") == -1:
            if return_num:
                href_text = int(href_text)
            years.append(href_text)

    return years


def fetch_days(station, year, return_num=False):
    """
    Fetches available days of PSE data for year of a station.

    :param station: station name
    :param year: year
    :param return_num: if True returns day as number instead of 3-character string (e.g. 1 instead of "001")
    :return: days of the year list (empty if station name or year are invalid)
    """
    # add "s" in front of station number
    station = str(station)
    if not station.startswith("s"):
        station = "s" + station

    try:
        url = "https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/data/xa/continuous_waveform/" \
              "{station}/{year}/".format(station=station, year=year)
        source = urlopen(url).read()
    except HTTPError:
        return []

    soup = bs.BeautifulSoup(source, "html.parser")

    days = []
    for a in soup.find_all("a", href=True):
        href_text = a.getText()
        if href_text.find("Parent") == -1:
            if return_num:
                href_text = int(href_text)
            days.append(href_text)

    return days


def fetch_data(stations=None, years=None, days=None, only_mid_period=True):
    """
    Fetches PSE data.

    :param stations: station name or station name list (only valid station names used), if None fetch from all available
                     stations
    :param years: year or year list, if None fetch for all available years
    :param days: day or day list, if None fetch for all available days
    """
    fetched_stations = fetch_stations(return_num=True)
    if stations is None:
        valid_stations = ["s" + str(station) for station in fetched_stations]  # all available stations
    else:
        if not isinstance(stations, list):
            stations = [stations]
        # only valid stations
        valid_stations = [str(station) for station in stations if int(str(station).lstrip("s")) in fetched_stations]

    for index_station, station in enumerate(valid_stations):
        fetched_years = fetch_years(station, return_num=False)
        if years is None:
            valid_years = fetched_years  # all available years
        else:
            if not isinstance(years, list):
                years = [years]
            # only valid years
            valid_years = [str(year) for year in years if str(year) in fetched_years]

        for index_year, year in enumerate(valid_years):
            fetched_days = fetch_days(station, year, return_num=True)
            if days is None:
                valid_days = ["%03d" % day for day in fetched_days]  # all available days
            else:
                if not isinstance(days, list):
                    days = [days]
                # # only valid days
                valid_days = ["%03d" % int(day) for day in days if int(day) in fetched_days]

            for index_day, day in enumerate(valid_days):
                # add "s" in front of station number
                if not station.startswith("s"):
                    station_name = "s" + station
                else:
                    station_name = station

                attempt = 0
                while attempt < 10:
                    try:
                        url = "https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/" \
                              "data/xa/continuous_waveform/" \
                              "{station}/{year}/{day}/".format(station=station_name, year=year, day=day)
                        source = urlopen(url).read()

                        soup = bs.BeautifulSoup(source, "html.parser")

                        for a in soup.find_all("a", href=True):
                            file = a.getText()
                            # only mid-period .mseed files
                            if only_mid_period:
                                keep = (file.find(".mseed") != -1) and (file.find(".mh") != -1)
                            # only .mseed files
                            else:
                                keep = file.find(".mseed") != -1
                            if keep:
                                directory_out = os.path.join(os.getcwd(), "data", station_name, year, day)
                                if not os.path.isdir(directory_out):
                                    os.makedirs(directory_out)
                                file_path_out = os.path.join(directory_out, file)

                                # download file
                                url = "https://pds-geosciences.wustl.edu" + a["href"]

                                urlretrieve(url, file_path_out)

                        print("Saved",
                              station,
                              "({station}/{stations})".format(station=index_station + 1, stations=len(valid_stations)),
                              year, "({year}/{years})".format(year=index_year + 1, years=len(valid_years)),
                              day, "({day}/{days})".format(day=index_day + 1, days=len(valid_days)))

                        break
                    # wrong day
                    except HTTPError:
                        return
                    # failed to fetch
                    except URLError:
                        time.sleep(5)
                    attempt += 1
                    if attempt == 10:
                        print("ERROR",
                              station,
                              "({station}/{stations})".format(station=index_station + 1, stations=len(valid_stations)),
                              year, "({year}/{years})".format(year=index_year + 1, years=len(valid_years)),
                              day, "({day}/{days})".format(day=index_day + 1, days=len(valid_days)))
                        break


if __name__ == "__main__":
   fetch_data("s11")
   fetch_data("s12")
   fetch_data("s14")
   fetch_data("s15")
   fetch_data("s16")