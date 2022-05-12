from os import path

from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
from zcrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.dc import EUDataCenter
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature

from packages.adapters.configuration.configuration import Configuration


def initialize():
    config = Configuration()
    """
    Create an instance of Logger Class that takes two parameters
    1 -> Level of the log messages to be logged. Can be configured by typing Logger.Levels "." and choose any level from the list displayed.
    2 -> Absolute file path, where messages need to be logged.
    """
    logger = Logger.get_instance(level=Logger.Levels.DEBUG,
                                 file_path=config.get('sdk', 'log_file_path'))

    # Create an UserSignature instance that takes user Email as parameter
    user = UserSignature(email=config.get('sdk', 'current_user_email'))

    """
    Configure the environment
    which is of the pattern Domain.Environment
    Available Domains: USDataCenter, EUDataCenter, INDataCenter, CNDataCenter, AUDataCenter
    Available Environments: PRODUCTION(), DEVELOPER(), SANDBOX()
    """
    environment = EUDataCenter.PRODUCTION()

    """
    Create a Token instance that takes the following parameters
    1 -> OAuth client id.
    2 -> OAuth client secret.
    3 -> REFRESH/GRANT token.
    4 -> token type.
    5 -> OAuth redirect URL.
    """
    token = OAuthToken(client_id=config.get('client', 'client_id'),
                       client_secret=config.get('client', 'client_secret'),
                       token=config.get('sdk', 'refresh_token'),
                       token_type=TokenType.REFRESH,
                       redirect_url=config.get('sdk', 'redirect_url'))

    """
    Create an instance of TokenStore
    1 -> Absolute file path of the file to persist tokens
    """
    store = FileStore(file_path=config.get('sdk', 'token_persistence_path'))

    """
    auto_refresh_fields (Default value is False)
        if True - all the modules' fields will be auto-refreshed in the background, every hour.
        if False - the fields will not be auto-refreshed in the background. The user can manually delete the file(s) or refresh the fields using methods from ModuleFieldsHandler(zcrmsdk/src/com/zoho/crm/api/util/module_fields_handler.py)

    pick_list_validation (Default value is True)
    A boolean field that validates user input for a pick list field and allows or disallows the addition of a new value to the list.
        if True - the zohoSDK validates the input. If the value does not exist in the pick list, the zohoSDK throws an error.
        if False - the zohoSDK does not validate the input and makes the API request with the user’s input to the pick list
    """
    sdk_config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)

    """
    The path containing the absolute directory path (in the key resource_path) to store user-specific files containing information about fields in modules. 
    """
    resource_path = config.get('sdk', 'resource_path')

    """
    Call the static initialize method of Initializer class that takes the following arguments
    1 -> UserSignature instance
    2 -> Environment instance
    3 -> Token instance
    4 -> TokenStore instance
    5 -> SDKConfig instance
    6 -> resource_path
    7 -> Logger instance. Default value is None
    8 -> RequestProxy instance. Default value is None
    """
    Initializer.initialize(user=user, environment=environment, token=token, store=store, sdk_config=sdk_config,
                           resource_path=resource_path, logger=logger)
