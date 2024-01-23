import logging
from typing import List, final
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor
from boto3 import client
from gspl.config.cli_config import config

import datetime


class BaseCommand(BaseModel):
    name: str = Field(default="", description="Nome do comando")
    info: List[str | int] | str = Field(default=None, description="Argumentos do comando")
    parallel: int = Field(default=1, description="Número de processos paralelos")

    class Config:
        arbitrary_types_allowed = True
        
    @property
    def args(self) -> List[str | int]:
        informed_args = []
        for i in self.info:
           informed_args.append(i.replace(" ", ""))
                
        return informed_args
        
    @property
    def logger(self):
        logger_name = f"{__name__}.{self.name}.{self.__class__.__name__}"

        # Usa um logger compartilhado para evitar duplicatas
        if logger_name not in logging.Logger.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.setLevel(config.logger.level)
            formatter = logging.Formatter(config.logger.formater())
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logging.getLogger(logger_name)
    
    @property
    def aws(service_name: str) -> client:
        """
        Retorna um client do AWS
        """
        if config.environment == "DEVELOPMENT":
            return client(
                service_name=service_name,
                region_name=config.aws.region,
                aws_access_key_id=config.aws.aws_access_key_id,
                aws_secret_access_key=config.aws.aws_secret_access_key,
                endpoint_url=config.aws.endpoint_url,
            )
        
        return client(
            service_name=service_name,
            region_name=config.aws.region,
            aws_access_key_id=config.aws.aws_access_key_id,
            aws_secret_access_key=config.aws.aws_secret_access_key,
        )
    @property
    def open_elastic(self):
        """
        Retorna um client do OpenSearch
        """
        from gspl.config.open_search import ClientOpenSearh
        return ClientOpenSearh.client()
    
    @classmethod
    def execute(cls):
        ...
            
    def _configure(self):
        pass
    
    def __hash__(self) -> int:
        return hash(f"{self.__class__.__name__}-{datetime.datetime.now()}")
    
    def _execute(self):
        # executa o metodo execute em paralelo ou não
        if self.parallel > 1:
            with ThreadPoolExecutor(max_workers=self.parallel) as executor:
                futures = [executor.submit(self.execute) for _ in range(self.parallel)]
                # Aguarda a conclusão de todas as execuções
                for future in futures:
                    future.result()
        else:
            self.execute()