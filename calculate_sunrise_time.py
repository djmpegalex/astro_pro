PY3 = True
from math import floor, pi, atan, tan, sin, asin, cos, acos
from datetime import timedelta

d2r = pi / 180


def day_of_year(d, m, y):
    return floor(275 * m / 9) - (floor((m + 9) / 12) * (1 + floor((y - 4 * floor(y / 4) + 2) / 3))) + d - 30


def time_calc(lat, lng, doy, td_utc, sunrise):
    # convert the longitude to hour value and calculate an approximate time
    lng_h = lng / 15
    t = doy + ((6 if sunrise else 18) - lng_h) / 24

    # m => Sun's mean anomaly
    m = (0.9856 * t) - 3.289

    # lk => Sun's true longitude
    lk = m + (1.916 * sin(m * d2r)) + (0.020 * sin(2 * m * d2r)) + 282.634
    lk += -360 if lk > 360 else 360 if lk < 360 else 0

    # ra = Sun's right ascension (right ascension value needs to be in the same quadrant as lk)
    ra = atan(0.91764 * tan(lk * d2r)) / d2r
    ra += -360 if ra > 360 else 360 if ra < 360 else 0
    ra += (floor(lk / 90) - floor(ra / 90)) * 90
    ra /= 15

    # sinDec, cosDec => Sine and Cosine of Sun's declination
    sin_dec = 0.39782 * sin(lk * d2r)
    cos_dec = cos(asin(sin_dec))

    # Sun's local hour angle
    cos_h = (cos(90.8333333333333 * d2r) - (sin_dec * sin(lat * d2r))) / (cos_dec * cos(lat * d2r))
    if sunrise and cos_h > 1:
        print('the sun never rises on this location (on the specified date)')

    elif not sunrise and cos_h < -1:
        print('the sun never sets on this location (on the specified date)')

    h = ((360 - (acos(cos_h) / d2r)) if sunrise else (acos(cos_h) / d2r)) / 15

    # Local mean time of rising/setting
    mean_t = h + ra - (0.06571 * t) - 6.622

    # adjust back to local standard time
    local = mean_t - lng_h + td_utc
    local += 24 if local < 0 else -24 if local > 24 else 0
    return local


def timed_date(date):
    return timedelta(seconds=date * 3600)


def get_calculate_sunrise(latitude, longitude, day_date, month_date, year_date, utc):
    lat = latitude
    lng = longitude
    d, m, y = day_date, month_date, year_date
    td_utc = utc
    sunrise_time = 0
    sunset_time = 0
    if 0 < d < 32 and 0 < m < 13:
        sunrise = time_calc(lat, lng, day_of_year(d, m, y), td_utc, True)
        sunset = time_calc(lat, lng, day_of_year(d, m, y), td_utc, False)

        sunrise_time = timed_date(sunrise).seconds
        sunset_time = timed_date(sunset).seconds

    return sunrise_time, sunset_time

# if __name__ == '__main__':
#     main()
