from enum import Enum
import logging
import json
from typing import List, Union

import requests
from pydantic import BaseModel
from slack_sdk.webhook import WebhookClient

from .config import (
    AUTH0_DOMAIN,
    AUTH0_PORTAL_AUDIENCE,
    AUTH0_PORTAL_M2M_CLIENT_ID,
    AUTH0_PORTAL_M2M_CLIENT_SECRET,
    BAD_ACTOR_API_URL,
    BAD_ACTOR_NOTIFICATION_URL,
)


class BadActorJudgmentType(int, Enum):
    information = 0
    unknown = 1
    good = 2
    suspect = 3
    bad = 4


class BadActorResponseItem(BaseModel):
    label: str
    value: Union[str, None]
    judgment: BadActorJudgmentType


class BadActorResponse(BaseModel):
    overall_judgment: BadActorJudgmentType
    auto_rejected: bool
    items: List[BadActorResponseItem]


EMOJI_MAP = {
    BadActorJudgmentType.good: ":white_check_mark: ",
    BadActorJudgmentType.bad: ":x: ",
    BadActorJudgmentType.suspect: ":eyes: ",
    BadActorJudgmentType.unknown: ":grey_question: ",
    BadActorJudgmentType.information: "",
}


class ConfigurationException(Exception):
    pass


class BadActor:
    def __init__(self, bad_actor_request):
        self.bad_actor_request = bad_actor_request
        self.transaction = None
        self.transaction_data = {}

        try:
            self.bad_actor_api_response = self._call_bad_actor_api(bad_actor_request)
        except Exception as error:
            logging.warning("Unable to call bad actor API: %s", error)
            self.bad_actor_api_response = None

    @property
    def quarantine(self):
        if not self.bad_actor_api_response:
            return False
        if self.bad_actor_api_response.overall_judgment >= BadActorJudgmentType.suspect:
            return True
        return False

    @staticmethod
    def _slackify_items(bad_actor_items) -> list:
        fields = []
        for bad_actor_item in sorted(bad_actor_items, key=lambda k: k.label):
            emoji = EMOJI_MAP[bad_actor_item.judgment]
            label = f"*{bad_actor_item.label}*: " if bad_actor_item.label else ""
            string = f"{emoji}{label}{bad_actor_item.value}"
            field = {"type": "mrkdwn", "text": string}
            fields.append(field)
        return fields

    def _slackify_all(self) -> list:

        # add another item for the Salesforce link
        txn_url = f"{self.transaction.sf.instance_url}/{self.transaction.id}"
        slackified_txn_link = f"<{txn_url}|Salesforce>"
        sf_link_item = BadActorResponseItem(
            label="",
            value=slackified_txn_link,
            judgment=BadActorJudgmentType.information,
        )
        self.bad_actor_api_response.items.append(sf_link_item)

        info_items = [
            x
            for x in self.bad_actor_api_response.items
            if x.judgment == BadActorJudgmentType.information
        ]
        judgment_items = [
            x
            for x in self.bad_actor_api_response.items
            if x.judgment != BadActorJudgmentType.information
        ]

        info_items = self._slackify_items(info_items)
        judgment_items = self._slackify_items(judgment_items)

        slack_block = [
            {
                "type": "section",
                "fields": info_items,
            },
            {
                "type": "section",
                "fields": judgment_items,
            },
        ]

        if self.bad_actor_api_response.auto_rejected:
            slack_block.append({
                "type": "section",
                "fields": [{
                    "type": "mrkdwn",
                    "text": "Donation auto-rejected"
                }]
            })
        else:
            slack_block.append({
                "type": "actions",
                "block_id": "choices",
                "elements": [
                    {
                        "action_id": "approve_new",
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Approve",
                        },
                        "style": "primary",
                        "value": json.dumps(self.transaction_data),
                    },
                    {
                        "action_id": "reject_new",
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "Reject"},
                        "style": "danger",
                        "value": json.dumps(self.transaction_data),
                    },
                ],
            })

        return slack_block

    def _send_to_slack(self):

        if not BAD_ACTOR_NOTIFICATION_URL:
            raise ConfigurationException("BAD_ACTOR_NOTIFICATION_URL unset")

        blocks = self._slackify_all()

        webhook = WebhookClient(BAD_ACTOR_NOTIFICATION_URL)
        response = webhook.send(blocks=blocks)
        logging.info(response)

    def notify_bad_actor(
            self,
            transaction,
            transaction_data):

        self.transaction = transaction
        self.transaction_data = transaction_data

        if self.bad_actor_api_response.overall_judgment < BadActorJudgmentType.suspect:
            logging.info("not a bad actor; returning")
            return

        logging.debug(self)
        self._send_to_slack()

        return

    @staticmethod
    def create_bad_actor_request(
        headers,
        captcha_token,
        email,
        amount,
        zipcode,
        first_name,
        last_name,
        remote_addr,
        reason,
    ) -> dict:

        referer = headers.get("Referer", None)

        x_forwarded_for = headers.get("X-Forwarded-For", None)
        cf_ip_country = headers.get("Cf-Ipcountry", None)

        ip = remote_addr
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]

        return {
            "email": email,
            "ip": ip,
            "country_code": cf_ip_country,
            "zipcode": zipcode,
            "given_name": first_name,
            "family_name": last_name,
            "referer": referer,
            "captcha_token": captcha_token,
            "reason": reason,
            "amount": amount,
        }

    @staticmethod
    def _call_bad_actor_api(request) -> Union[BadActorResponse, None]:

        if not BAD_ACTOR_API_URL:
            raise ConfigurationException("BAD_ACTOR_API_URL unset")

        if not all(
            [
                AUTH0_DOMAIN,
                AUTH0_PORTAL_AUDIENCE,
                AUTH0_PORTAL_M2M_CLIENT_ID,
                AUTH0_PORTAL_M2M_CLIENT_SECRET,
            ]
        ):
            raise ConfigurationException("AUTH0 variable unset")

        payload = {
            "client_id": AUTH0_PORTAL_M2M_CLIENT_ID,
            "client_secret": AUTH0_PORTAL_M2M_CLIENT_SECRET,
            "audience": AUTH0_PORTAL_AUDIENCE,
            "grant_type": "client_credentials",
        }

        auth0_response = requests.post(
            url=f"https://{AUTH0_DOMAIN}/oauth/token", json=payload
        ).json()
        access_token = auth0_response["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        logging.info(request)
        response = requests.post(url=BAD_ACTOR_API_URL, headers=headers, json=request)
        response = response.json()
        logging.info(response)

        return BadActorResponse.parse_obj(response)
