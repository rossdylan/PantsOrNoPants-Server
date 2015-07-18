import ponp_server.localization as locale
from ponp_server.database import db_session
from ponp_server.models.users import User


def lang_parser(lang):
    lang = lang.lower()
    print lang
    if lang not in locale.Pants:
        raise ValueError(
            'Language Must be one of {0}'.format(locale.Pants.iterkeys()))
    return lang


def gender_parser(gender):
    gender = gender.lower()
    if gender not in locale.Genders:
        raise ValueError('Gender must be one of {0}'.format(locale.Genders))
    return gender


def inclination_parser(incl):
    incl = incl.lower()
    if incl not in locale.Inclinations:
        raise ValueError(
            'Inclination must be one of {0}'.format(locale.Inclinations))
    return incl


def apikey_parser(key):
    query = db_session.query(User).filter(User.apikey == key)
    if query.count() == 0:
        raise ValueError('Please enter a valid api key')
    return key
