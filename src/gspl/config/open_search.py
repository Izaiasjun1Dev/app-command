from typing import List
from pydantic import BaseModel, Field
from opensearchpy import OpenSearch
from gspl.config.cli_config import config


class ClientOpenSearh(BaseModel):
    
    host: List[dict] = Field(
    default=[
        {
            'host': config.open_elastic.host, 
            'port': config.open_elastic.port,
        }
    ], 
    description="Hosts do OpenSearch")
    
    @classmethod
    def client(cls):
        return OpenSearch(
            hosts=[{
                'host': config.open_elastic.host, 
                'port': config.open_elastic.port,
            }],
            http_auth = config.open_elastic.auth,
            use_ssl = config.open_elastic.use_ssl,
            verify_certs = config.open_elastic.verify_certs,
            ssl_assert_hostname = config.open_elastic.ssl_assert_hostname,
            ssl_show_warn = config.open_elastic.ssl_show_warn,
        )
