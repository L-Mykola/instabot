import random
import time

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

from loguru import logger


class User:

    def __init__(self, settings):
        self.settings = settings
        self.client = Client()
        if settings.proxy['set_proxy']:
            self.client.set_proxy(f"{settings.proxy['proxy_url']}")

    def login_user(self, username, password):
        """
        Attempts to login to Instagram using either the provided session information
        or the provided username and password.
        """

        try:
            session = self.client.load_settings(f"sessions/{username}_session.json")
        except Exception as e:
            session = None
            logger.warning("Session file not found, need to login via username and password")

        login_via_session = False
        login_via_pw = False

        if session:
            try:
                self.client.set_settings(session)
                self.client.login(username, password)

                try:
                    self.client.get_timeline_feed()
                except LoginRequired:
                    logger.info("Session is invalid, need to login via username and password")

                    old_session = self.client.get_settings()

                    self.client.set_settings({})
                    self.client.set_uuids(old_session["uuids"])

                    self.client.login(username, password)

                login_via_session = True
            except Exception as e:
                logger.info(f"Couldn't login user using session information: {e}")

        if not login_via_session:
            try:
                logger.info(f"Attempting to login via username and password. username: {username}")
                if self.client.login(username, password):
                    login_via_pw = True
            except Exception as e:
                logger.info(f"Couldn't login user using username and password: {e}")

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")

    def simulate_user_behavior(self, client):
        """
        A function for simulating user behavior, performing like/subscribe actions.
        :param client:
        :return:
        """
        target_ids = self.settings.target_ids
        random.shuffle(target_ids)
        for user_id in target_ids[:self.settings.max_actions_per_run]:
            action = random.choice(["like", "follow"])
            try:
                if action == "like":
                    medias = client.user_medias_v1(user_id, amount=1)
                    if medias:
                        client.media_like(medias[0].id)
                        logger.info(f"[{client.username}] 👍 Like the post [userId:{user_id}]")
                elif action == "follow":
                    client.user_follow(user_id)
                    logger.info(f"[{client.username}] ➕ Follow to [userId:{user_id}]")
            except Exception as e:
                logger.error(f"[{client.username}] ⚠️ Error while performing an action ({action}): {e}")

            delay = random.randint(self.settings.min_delay, self.settings.max_delay)
            logger.info(f"⏱ Pause {delay} sec.")
            time.sleep(delay)

    def run_actions(self, account):
        """
        A function for running user actions
        :return:
        """
        try:
            self.login_user(account['username'], account['password'])
            logger.info(f"🔐 Login as {account['username']}")
            self.simulate_user_behavior(self.client)
            self.client.logout()
        except Exception as e:
            logger.error(f"❌ {account['username']} — login error: {e}")