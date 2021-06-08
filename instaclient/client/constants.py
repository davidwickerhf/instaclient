#!/usr/bin/env python
#
# Unofficial Instagram Python client. Built with the use of the selenium,
# and requests modules.
# Copyright (C) 2015-2021
# David Henry Francis Wicker <wickerdevs@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
class Paths:
    # LOGIN PROCEDURE
    LOGIN_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]/div'
    USERNAME_INPUT = '//input[@name="username"]'
    PASSWORD_INPUT = '//input[@name="password"]'
    # Suscpicious Activity Dialogue
    SEND_CODE = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
    SECURITY_CODE_INPUT = '//input[@name="security_code" or @class="_281Ls zyHYP"]'
    INPUT_CODE_BTN = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
    INVALID_CODE = '//div[@class="_3_2jD" and @id="form_error"]'
    ERROR_SENDING_CODE = '//div[@class="_3_2jD" and @id="form_error"]//descendant::p'
    RESEND_CODE_BTN = '//p[@class="GusmU  t_gv9    "]//descendant::a'
    SELECT_EMAIL_BTN = '//label[@class="UuB0U " and @for="choice_1"]//descendant::div'
    BACK_BTN = '//svg[@class="_8-yf5 "]'
    SECURITY_CODE_BTN = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
    # 2FA Verification
    VERIFICATION_CODE = '//input[@name="verificationCode"]'
    VERIFICATION_CODE_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]'
    # Pop-Ups
    DISMISS_DIALOGUE = '//button[@class="aOOlW   HoLwm "]'

    # NAV TO USER PROCEDURE 
    WAIT_BEFORE_LOGIN = '//p[contains(text(), "Please wait")]'
    INCORRECT_USERNAME_ALERT = '//p[@role="alert" and @id="slfErrorAlert"]'
    INCORRECT_PASSWORD_ALERT = '//div[@class="piCib"]'
    INCORRECT_PASSWORD_ALERT_BTNS = '{}//button[contains(@class, "aOOlW")]'
    ALERT = '//*[@id="slfErrorAlert" or @id="twoFactorErrorAlert"]'
    PAGE_NOT_FOUND = '//h2[@class="_7UhW9      x-6xq    qyrsm KV-D4          uL8Hv     l4b0S    "]'
    PRIVATE_ACCOUNT_ALERT = '//h2[@class="rkEop"]'

    # SEND DM PROCEDURE
    SEARCH_USER_INPUT = '//input[@name="queryBox"]'
    USER_DIV = '//div[@class="-qQT3"]'
    USER_DIV_USERNAME = '//div[@class="_7UhW9   xLCgt       qyrsm KV-D4          uL8Hv         "]'
    NEXT_BUTTON = '//div[@class="rIacr"]'

    DM_TEXT_AREA = '//div[@class="X3a-9"]//descendant::textarea'
    SEND_DM_BTN = '//div[@class="X3a-9"]//descendant::button'

    # CHECK LOGIN STATUS
    NAV_BAR = '//div[@data-testid="mobile-nav-logged-in" and @class="BvyAW"]'

    # ENGAGEMENT PROCEDURES
    # Post Interactions
    POST_DIV = '//a[@href="/p/{}/"]'
    COMMENT_TEXT_AREA = '//textarea[@class="Ypffh"]'
    SEND_COMMENT_BTN = '//button[@class="sqdOP yWX7d    y3zKF     "]'
    LIKE_BTN = '//span[@class="fr66n"]//descendant::button'
    COMMENT_BTN = '//span[@class="_15y0l"]'
    SHARE_POST_BTN = '//*[@id="react-root"]/section/main/div/div/article/div[3]/section[1]/span[3]/button' # TODO critical

    # Follow User Procedure
    FOLLOW_BTN = '//button[@class="sqdOP  L3NKy _4pI4F  y3zKF     " or @class="_5f5mN       jIbKX  _6VtSN     yZn4P   "]'
    UNFOLLOW_BTN = '//button[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]//descendant::span'
    CONFIRM_UNFOLLOW_BTN = '//button[@class="aOOlW -Cab_   "]'
    REQUESTED_BTN = '//div[@class=" ffKix "]//descendant::button'
    MESSAGE_USER_BTN = '//button[@class="sqdOP  L3NKy _4pI4F   _8A5w5    "]'
    
    # USER ACCOUNT DMs PAGE
    DM_LIST_DIV = '//div[@class="N9abW"]//descendant::div'
    DM_USERNAME_DIV = '//div[@class="_7UhW9   xLCgt      MMzan  KV-D4              fDxYl     "]'

    # GENERAL
    DIALOGUE = '//button[contains(text(), "Cancel") or contains(text(), "Not Now")]'
    USE_THE_APP = '//button[@class="sqdOP yWX7d    y3zKF   cB_4K  "]' #TODO
    X = '//div[@class="storiesSpriteX__outline__44 u-__7"]'
    USE_APP_BAR = '//button[@class="dCJp8 "]'
    COOKIES_LINK = '//a[contains(@heref, "cookies") or contains(text(), "Cookie")]'
    ACCEPT_COOKIES = '//button[@class="aOOlW  bIiDR  "]'
    SETTINGS_BTN = '//button[@class="Q46SR"]'
    BUTTON = '//button[text()="{}"]'
    NOT_NOW_BTN = '//button[@class="aOOlW   HoLwm "]'
    SAVE_INFO_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]'
    RESTRICTION_DIALOG = '//div[@class="_7UhW9   xLCgt      MMzan   _0PwGv         uL8Hv         " and contains(text(), "restrict")]'
    RESTRICTION_DIALOGUE_BTNS = '//div[@class="pbNvD  fPMEg    " and @role="dialog"]//descendant::button'
    BLOCK_DIV = '//div[@class="_7UhW9    vy6Bb     MMzan  KV-D4          uL8Hv     l4b0S    " and contains(text(), "unusual activity")]'
    QUERY_ELEMENT = '//body//descendant::pre'
    # Navigation Bar
    HOME_BTN = '//a[@href="/"]'
    EXPLORE_BTN = '//a[@href="/explore/"]'

    # SETTINGS OPTIONS
    LOG_OUT_BTN = '//a[@class="_34G9B H0ovd"]'
    CONFIRM_LOGOUT_BTN = '//button[@class="aOOlW  bIiDR  "]'

    # SCRAPING
    # Scrape Followers Procedure
    FOLLOWERS_BTN = '//a[contains(@href, "followers")  and not(contains(@href, "mutual"))]'
    FOLLOWED_BTN = '//a[contains(@href, "following") and not(contains(@href, "mutual"))]'
    FOLLOWERS_LIST_MAIN = '//main[@role="main"]'
    FOLLOWERS_LIST = '//ul[@class=" jjbaz _6xe7A"]'
    FOLLOWER_USER_DIV = '{}//li'.format(FOLLOWERS_LIST)
    FOLLOWER_COUNT = '{}//span[@class="g47SY lOXF2"]'.format(FOLLOWERS_BTN)

    # Scrape User Posts Procedure
    SHORTCODE_DIV = '//div[@class="v1Nh3 kIKUG  _bz0w"]//descendant::a'

    # EXPLORE PAGE
    # //*[@id="react-root"]/section/nav[1]/div/header/div/h1/div/div/div/div/label/input
    # EXPLORE_SEARCH_INPUT = '//label[@class="NcCcD"]//descendant::input' # TODO this is not working!
    EXPLORE_SEARCH_INPUT = '//*[@id="react-root"]/section/nav[1]/div/header/div/h1/div/div/div/div/label/input'
    SEARCH_USER_DIV = '//div[@class="_7UhW9   xLCgt       qyrsm KV-D4          uL8Hv         " and contains(text(), {})]'

    

class ClientUrls:
    CHALLENGE_URL = 'https://www.instagram.com/challenge'
    LOGIN_URL='https://www.instagram.com/accounts/login/'
    NAV_USER='https://www.instagram.com/{}/'
    NEW_DM = 'https://www.instagram.com/direct/new/'
    SEARCH_TAGS='https://www.instagram.com/explore/tags/{}/'
    FOLLOWERS_URL = 'https://www.instagram.com/{}/followers/'
    HOME_URL =  'https://www.instagram.com'
    LOGIN_THEN_USER = 'https://www.instagram.com/accounts/login/?next=/{}/'
    SECURITY_CODE_URL = 'https://www.instagram.com/challenge/'
    DM_URL  = 'https://www.instagram.com/direct/t/'
    POST_URL = 'https://www.instagram.com/p/{}/'
    COMMENTS_URL = 'https://www.instagram.com/p/{}/comments/'
    EXPLORE_PAGE = 'https://www.instagram.com/explore/'
    LOCATION_PAGE = 'https://www.instagram.com/explore/locations/{}/{}/'


class GraphUrls:
    GRAPH_USER='https://www.instagram.com/{}/?__a=1'
    GRAPH_TAGS='https://www.instagram.com/explore/tags/{}/?__a=1'
    GRAPH_ACTIVITY = 'https://www.instagram.com/accounts/activity/?__a=1'
    GRAPH_POST = 'https://www.instagram.com/p/{}/?__a=1'
    GRAPH_SEARCH = 'https://www.instagram.com/web/search/topsearch/?query={}'
    GRAPH_LOCATION = 'https://www.instagram.com/explore/locations/{}/{}/?__a=1'

    GRAPH_FIRST_FOLLOWERS = 'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}&variables=%7B%22id%22%3A%22{ID}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%7D'
    GRAPH_CURSOR_FOLLOWERS = 'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}&variables=%7B%22id%22%3A%22{ID}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A50%2C%22after%22%3A%22{END_CURSOR}%3D%3D%22%7D'

    GRAPH_FIRST_FOLLOWING = 'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}8&variables=%7B%22id%22%3A%22{ID}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A50%7D'
    GRAPH_CURSOR_FOLLOWING = 'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}8&variables=%7B%22id%22%3A%22{ID}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A50%2C%22after%22%3A%22{END_CURSOR}%3D%3D%22%7D'


class QueryHashes:
    FOLLOWERS_HASH = '5aefa9893005572d237da5068082d8d5'
    FOLLOWING_HASH = '3dec7e2c57367ef3da3d987d89f9dbc'