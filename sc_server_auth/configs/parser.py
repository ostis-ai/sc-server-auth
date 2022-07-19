import toml

import sc_server_auth.configs.constants as c
import sc_server_auth.configs.models as m
from sc_server_auth.configs.paths import DEV_CONFIG_PATH


class Parser:  # pylint: disable=too-few-public-methods
    _config: m.Config = None

    @classmethod
    def _parse(cls):
        data = toml.load(DEV_CONFIG_PATH)
        data_common = data[c.COMMON]
        data_tokens = data[c.TOKENS]
        data_server = data[c.SERVER]
        # data_sc_server = data[c.SC_SERVER]
        data_database = data[c.DATABASE]
        data_postgres = data_database[c.POSTGRES]

        cls._config = m.Config(
            common=m.CommonParams(log_level=data_common[c.LOG_LEVEL]),
            tokens=m.TokensParams(
                access_token_life_span=data_tokens[c.ACCESS_TOKEN_LIFE_SPAN],
                refresh_token_life_span=data_tokens[c.REFRESH_TOKEN_LIFE_SPAN],
                bits=data_tokens[c.BITS],
                issuer=data_tokens[c.ISSUER],
            ),
            server=m.ServerParams(protocol=data_server[c.PROTOCOL], host=data_server[c.HOST], port=data_server[c.PORT]),
            # sc_server=m.ScServerParams(
            #     protocol=data_sc_server[c.PROTOCOL],
            #     host=data_sc_server[c.HOST],
            #     port=data_sc_server[c.PORT],
            #     ws_json_url=data_sc_server[c.WS_JSON_URL],
            #     sc_create_user_endpoint=data_sc_server[c.SC_CREATE_USER_ENDPOINT],
            # ),
            database=m.DatabaseParams(
                database=m.Database(data_database[c.DATABASE]),
                user=data_postgres[c.USER],
                password=data_postgres[c.PASSWORD],
                name=data_postgres[c.NAME],
                host=data_postgres[c.HOST],
                isolation_level=m.IsolationLevel(data_postgres[c.ISOLATION_LEVEL]),
            ),
        )

    @classmethod
    def get_config(cls) -> m.Config:
        if cls._config is None:
            cls._parse()
        return cls._config


get_config = Parser.get_config
