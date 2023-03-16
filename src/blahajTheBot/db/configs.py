import boto3
from dotenv import load_dotenv
import logging


class Configs_DB:
    def __init__(self) -> None:
        load_dotenv()
        self.dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        self.table = self.dynamodb.Table('blahajthebot_configs')

    def get_config(self, guild_id: int, config_name: str) -> str | None:
        """Gets a config from the DB. Returns None if not found otherwise returns the config string"""
        logging.debug(
            f"Getting config ({config_name}) for {guild_id} from DB...")
        response = self.table.get_item(
            Key={
                'guild_id': guild_id,
                'config_name': config_name
            }
        )
        try:
            item = response['Item']['config_value']
        except KeyError:
            item = None
        return item

    def set_config(self, guild_id: int, config_name: str, config_value: str) -> bool:
        """Sets a config to the specified value. Returns True if successful, False if not"""
        logging.debug(
            f"Setting config ({config_name}) for {guild_id} to {config_value} in DB...")
        response = self.table.put_item(
            Item={
                'guild_id': guild_id,
                'config_name': config_name,
                'config_value': config_value
            }
        )
        # maybe will work?
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
