from enum import Enum
from colorama import Fore, Style
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel


class Environment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

class CmdConfig(BaseModel):
    commands_path: str = Field(default="commands")
    
class LoggerConfig(BaseModel):
    level: str = Field(default="INFO")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    datefmt: str = Field(default="%d-%b-%y %H:%M:%S")
    
    def formater(self, worker_name: str = f"{__name__}"):
        if config.environment == Environment.DEVELOPMENT:
            return f"{Fore.GREEN}%(asctime)s{Style.RESET_ALL} - {Fore.BLUE}%(name)s{Style.RESET_ALL} - {Fore.YELLOW}%(levelname)s{Style.RESET_ALL} - %(message)s"
        
        return self.format
    
class ElasticConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=9200)
    scheme: str = Field(default="http")
    
    def get_url(self):
        return f"{self.scheme}://{self.host}:{self.port}"
    
class ExitCode(Enum):
    SUCCESS = 0
    ERROR = 1
    FAILURE = 2
    NOT_IMPLEMENTED = 3
    NOT_FOUND = 4
    INVALID_INPUT = 5
    INVALID_OUTPUT = 6
    INVALID_CONFIG = 7
    INVALID_STATE = 8
    INVALID_OPERATION = 9    
    
class Application(BaseSettings):
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    name: str = Field(default="gspl", env="APPLICATION_NAME")
    version: str = Field(default="0.0.1", env="APPLICATION_VERSION")
    cmd: CmdConfig = Field(default=CmdConfig())
    logger: LoggerConfig = Field(default=LoggerConfig())
    elastic: ElasticConfig = Field(default=ElasticConfig())
    exit_code: ExitCode = Field(default=ExitCode.SUCCESS)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


load_dotenv(verbose=True)

config = Application()