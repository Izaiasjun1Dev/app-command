from importlib.util import module_from_spec, spec_from_file_location
import logging
from os import listdir
from gspl.console.utils import fromcwd
from gspl.config.cli_config import config

logger = logging.getLogger(__name__)

def available_commands():
    """
    Lista os comandos disponíveis
    """
    try:
        for command in listdir(fromcwd(config.cmd.commands_path)):
            yield command.replace(".py", "").replace("_", "-")
    except Exception as e:
        logger.error(e)
        
def exec_command(
    command: str,
    arg,
    parallel: int = 1,
):
    """
    Executa um comando
    """
    try:
        
        spec = spec_from_file_location(
            command,
            fromcwd(f"{config.cmd.commands_path}/{command}.py")
        )
        modulo = module_from_spec(spec)
        spec.loader.exec_module(modulo)
        
        from gspl.console.commands.command import BaseCommand
        cmd: BaseCommand = modulo.Command(
            name=command.replace("_", "-"),
            arg=arg,
            parallel=parallel
        )
        
        cmd._execute()
        
    except Exception as e:
        logger.error(e)
        raise e
        
        