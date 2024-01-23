from importlib.util import module_from_spec, spec_from_file_location
import logging
from os import listdir
import time
from gspl.console.utils import fromcwd
import typer
from colorama import Fore, Style
from gspl.config.cli_config import config
from tqdm import tqdm
import emoji

def start_new_project(
    path: str, 
    name: str, 
    description: str
):
    """
    Cria um novo projeto
    """
    try:
        # exibe o loading
        with typer.progressbar(
            length=100,
            label="Criando projeto",
            show_eta=False,
            show_percent=True,
            show_pos=False,
            width=30,
            color=True,
            fill_char=emoji.emojize(":rocket:"),
        ) as progress:
            ...
    except Exception as e:
        raise e
def process_multiple_arguments(value: str):
    """
    Processa argumentos múltiplos
    """
    if value is None or value == "":
        return []
    
    return value.split(",") \
        or value.split(" ") \
            or value.split(", ")


def available_commands(command_name: str = None):
    """
    retorna os comandos disponíveis
    caso o command_name seja != de None, retorna apenas true caso ele seja encontrado
    """
    commands = listdir(fromcwd(config.cmd.commands_path))
    
    if command_name is not None:
        return [
            command.replace(".py", "")
            .replace("_", "-") for command in commands
        ]
    
    typer.echo(f"{Fore.CYAN}Comandos disponíveis:{Style.RESET_ALL}\n")
    for idx, command in tqdm(enumerate(commands, start=1)):
        typer.echo(f"{idx}. {Fore.GREEN}{command.replace('.py', '').replace('_', '-')}{Style.RESET_ALL}\n")
    
    
def exec_command(
    command_name: str,
    info: list = [],
    parallel: int = 1,
):
    """
    Executa um comando
    """
    try:
        module_name = f"{config.cmd.commands_path}/{command_name}.py"
        
        spec = spec_from_file_location(
            module_name,
            module_name
        )
        
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        
        from gspl.console.commands.command import BaseCommand
        
        command: BaseCommand = getattr(module, "Command")(name=command_name, info=info, parallel=parallel)
        command._execute()
        
    except Exception as e:
        raise e
        
        