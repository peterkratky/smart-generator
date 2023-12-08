from enum import Enum


class TemplateTableMode(str, Enum):
    DEFAULT = "DEFAULT"
    ID = "ID"
    LONGITUDE = "LONGITUDE"
    LATITUDE = "LATITUDE"


class TimeseriesUnit(str, Enum):
    MILLISECOND = "MILLISECOND"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"
