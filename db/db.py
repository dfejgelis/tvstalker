# -*- coding: utf-8 -*-

import datetime

import model


def get_tv_show(title):
    serie = model.Serie.all()
    serie.filter('name =', title)
    if serie.count() == 0:
        return None
    return serie[0]


def get_user_shows(user):
    following = model.FollowingShows.all()
    following.filter('login =', user)
    if following.count() == 0:
        return []
    return following


def get_user_shows_by_date(user, date):
    following = model.FollowingShows.all()
    following.filter('login =', user)
    if following.count() == 0:
        return []

    user_shows = []
    for follow in following:
        season = get_last_season(follow.serie)
        if season is None:
            continue

        episodes = model.Episode().all()
        episodes.filter('season =', season)
        episodes.filter('airdate =', date)
        if episodes.count() != 0:
            user_shows.append(episodes[0])
    return user_shows


def check_username_is_valid(username):
    account = model.StalkerLogin.all()
    account.filter('username = ', username)
    if account.count() == 0:
        return (True and username.isalnum())
    return False


def clean_previous_activation(email):
    activate = model.ValidateUser.all()
    activate.filter('email = ', email)
    for active in activate:
        active.delete()


def get_activation_account(email, code):
    activate = model.ValidateUser.all()
    activate.filter('validate_code = ', code)
    activate.filter('email = ', email)
    if activate.count() == 0:
        return None
    return activate[0]


def is_show_in_db(source_url):
    serie = model.Serie.all()
    serie.filter('source_url =', source_url)
    if serie.count() == 0:
        return None
    return serie[0]


def get_last_season(show):
    season = model.Season.all()
    season.filter('serie =', show)
    season.filter('nro =', show.last_season)
    if season.count() == 0:
        return None
    return season[0]


def get_episodes_for_season(season):
    episodes = model.Episode.all()
    episodes.filter('season =', season)
    episodes.order('nro')
    return episodes


def get_episodes_for_season_and_nro(season, nro):
    episodes = model.Episode.all()
    episodes.filter('season =', season)
    episodes.filter('nro =', nro)
    if episodes.count() == 0:
        return None
    return episodes[0]


def obtain_most_recent_episode(show=None, show_title=''):
    if show is None:
        show = get_tv_show(show_title)
    season = get_last_season(show)
    if season is None:
        return None

    episodes = model.Episode().all()
    episodes.filter('season =', season)
    episodes.filter('airdate >=', datetime.date.today())
    episodes.order('airdate')
    if episodes.count() == 0:
        return None
    return episodes[0]


def is_already_following(user, show):
    following = model.FollowingShows.all()
    following.filter('login =', user)
    following.filter('serie =', show)
    if following.count() == 0:
        return None
    return following[0]


def get_profile(user):
    profile = model.User.all()
    profile.filter('login =', user)
    if profile.count() == 0:
        return None
    return profile[0]


def check_email_is_valid(email):
    profile = model.User.all()
    profile.filter('email =', email)
    if profile.count() == 0:
        return True
    return False


def is_valid_email_reset(email):
    profile = model.User.all()
    profile.filter('email =', email)
    if profile.count() == 0:
        return None
    return profile[0]


def get_image_url(image_name):
    published = model.PublishedImages.all()
    published.filter('image_name =', image_name)
    if published.count() == 0:
        return None
    return published[0].url
