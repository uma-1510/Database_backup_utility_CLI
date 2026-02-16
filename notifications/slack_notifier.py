import requests
from core.interfaces import NotificationInterface


class SlackNotifier(NotificationInterface):

    def __init__(self, webhook_url, logger):
        self.webhook_url = webhook_url
        self.logger = logger

    def send(self, message: str):
        response = requests.post(
            self.webhook_url,
            json={"text": message}
        )
        if response.status_code != 200:
            raise Exception("Slack notification failed")
        self.logger.info("Slack notification sent")
