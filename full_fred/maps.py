import os
from .tags import Tags


class Maps(Tags):
    def __init__(self):
        """
        FRED Maps API (GeoFRED) — geographic cross-sectional economic data.
        Provides regional data, series group metadata, and GeoJSON shape files.
        FRED Maps web service endpoint: geofred/
        https://fred.stlouisfed.org/docs/api/geofred/
        """
        super().__init__()
        self.__geo_url_base = "https://api.stlouisfed.org/geofred/"
        self.maps_stack = dict()

    def _make_geo_request_url(self, var_url: str) -> str:
        key_to_use = self._viable_api_key()
        base = self.__geo_url_base + var_url + "&file_type=json&api_key="
        if key_to_use == "env":
            try:
                return base + os.environ["FRED_API_KEY"]
            except KeyError as e:
                print(e, " no longer found in environment")
        if key_to_use == "file":
            return base + self._read_api_key_file()

    def _fetch_geo_data(self, url_prefix: str) -> dict:
        url = self._make_geo_request_url(url_prefix)
        json_data = self._get_response(url)
        if json_data is None:
            print("Data could not be retrieved, returning None")
            return
        return json_data

    def get_geo_series_group(
        self,
        series_id: str,
    ) -> dict:
        """
        Get the series group and metadata for a FRED series. Use this to find
        the series_group, region_type, and date range needed for get_regional_data.

        Parameters
        ----------
        series_id: str
            The FRED series ID.

        Returns
        -------
        dict
            Series group metadata including title, region_type, season, units,
            frequency, min_date, max_date, and series_group.

        Notes
        -----
        FRED Maps web service endpoint: geofred/series/group
        https://fred.stlouisfed.org/docs/api/geofred/series_group.html

        Examples
        --------
        >>> fred.get_geo_series_group(series_id="SMU56000000500000001a")
        {'series_group': {'title': 'All Employees: Total Private',
        'region_type': 'state', 'series_group': '1223', 'season': 'NSA',
        'units': 'Thousands of Persons', 'frequency': 'a',
        'min_date': '1990-01-01', 'max_date': '2022-01-01'}}
        """
        self._viable_api_key()
        url_prefix = self._append_id_to_url(
            "series/group?series_id=", a_str_id=series_id
        )
        self.maps_stack["get_geo_series_group"] = self._fetch_geo_data(url_prefix)
        return self.maps_stack["get_geo_series_group"]

    def get_geo_series(
        self,
        series_id: str,
        date: str = None,
        start_date: str = None,
    ) -> dict:
        """
        Get cross-sectional geographic data for a FRED series at a given date.

        Parameters
        ----------
        series_id: str
            The FRED series ID.
        date: str, default None
            The date for which to retrieve data, formatted as "YYYY-MM-DD".
            If None, FRED will use the most recent available date.
        start_date: str, default None
            The start date of the observation period, formatted as "YYYY-MM-DD".

        Returns
        -------
        dict
            Geographic cross-sectional data including meta and data keys.
            Each observation contains region, code, value, series_id, and date.

        Notes
        -----
        FRED Maps web service endpoint: geofred/series/data
        https://fred.stlouisfed.org/docs/api/geofred/series_data.html

        Examples
        --------
        >>> fred.get_geo_series(series_id="WIPCPI", date="2012-01-01")
        {'meta': {'title': 'Per Capita Personal Income by State',
        'region': 'state', 'seasonality': 'Not Seasonally Adjusted', ...},
        'data': {'2012-01-01': [{'region': 'Alabama', 'code': 'AL',
        'value': '36132', 'series_id': 'ALPCPI'}, ...]}}
        """
        self._viable_api_key()
        url_prefix = self._append_id_to_url(
            "series/data?series_id=", a_str_id=series_id
        )
        optional_args = {
            "&date=": date,
            "&start_date=": start_date,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.maps_stack["get_geo_series"] = self._fetch_geo_data(url)
        return self.maps_stack["get_geo_series"]

    def get_regional_data(
        self,
        series_group: str,
        date: str = None,
        start_date: str = None,
        region_type: str = None,
        units: str = None,
        frequency: str = None,
        season: str = None,
    ) -> dict:
        """
        Get cross-sectional regional data for a series group.

        Parameters
        ----------
        series_group: str
            The ID for a group of related geographic series. Retrieve via
            get_geo_series_group.
        date: str, default None
            The date for which to retrieve data, formatted as "YYYY-MM-DD".
        start_date: str, default None
            The start date of the observation period, formatted as "YYYY-MM-DD".
        region_type: str, default None
            The type of region. Can be one of "country", "state", "county",
            "msa", "frb", "necta", "bea", "censusregion", "censusdivision".
        units: str, default None
            The units of the data series, e.g. "Dollars".
        frequency: str, default None
            The frequency of the data. Can be "d", "w", "bw", "m", "q",
            "sa", or "a".
        season: str, default None
            The seasonality of the series. Can be "SA", "NSA", "SSA",
            "SAAR", or "NSAAR".

        Returns
        -------
        dict
            Regional cross-sectional data with meta and data keys.

        Notes
        -----
        FRED Maps web service endpoint: geofred/regional/data
        https://fred.stlouisfed.org/docs/api/geofred/regional_data.html

        Examples
        --------
        >>> params = {
        ...     "series_group": "882",
        ...     "date": "2013-01-01",
        ...     "region_type": "state",
        ...     "units": "Dollars",
        ...     "frequency": "a",
        ...     "season": "NSA",
        ... }
        >>> fred.get_regional_data(**params)
        {'meta': {'title': 'Per Capita Personal Income', 'region': 'state',
        'seasonality': 'Not Seasonally Adjusted', 'units': 'Dollars',
        'frequency': 'Annual', ...}, 'data': {'2013-01-01': [...]}}
        """
        self._viable_api_key()
        url_prefix = self._append_id_to_url(
            "regional/data?series_group=", a_str_id=series_group
        )
        optional_args = {
            "&date=": date,
            "&start_date=": start_date,
            "&region_type=": region_type,
            "&units=": units,
            "&frequency=": frequency,
            "&season=": season,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.maps_stack["get_regional_data"] = self._fetch_geo_data(url)
        return self.maps_stack["get_regional_data"]

    def get_shape_files(
        self,
        shape: str,
    ) -> dict:
        """
        Get GeoJSON shape files for a given geographic boundary type.

        Parameters
        ----------
        shape: str
            The type of geographic boundary. Can be one of "country", "state",
            "county", "msa", "frb", "necta", "bea", "censusregion",
            "censusdivision".

        Returns
        -------
        dict
            GeoJSON FeatureCollection with "type" and "features" keys.

        Notes
        -----
        FRED Maps web service endpoint: geofred/shapes/file
        https://fred.stlouisfed.org/docs/api/geofred/shapes.html

        Examples
        --------
        >>> fred.get_shape_files(shape="state")
        {'type': 'FeatureCollection', 'features': [{'type': 'Feature',
        'geometry': {...}, 'properties': {'GEOID': '01', 'NAME': 'Alabama',
        ...}}, ...]}
        """
        self._viable_api_key()
        url_prefix = self._append_id_to_url(
            "shapes/file?shape=", a_str_id=shape
        )
        self.maps_stack["get_shape_files"] = self._fetch_geo_data(url_prefix)
        return self.maps_stack["get_shape_files"]
