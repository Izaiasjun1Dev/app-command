
import typer
from colorama import Fore, Style
from gspl.config.cli_config import config
from gspl.console.commands import cmd
from gspl.console.application import Application

        
app = Application()

@app.command()
def version():
    """
    Exibe a versão do gspl
    """
    typer.echo(
        f"{Fore.GREEN}{config.name}{Style.RESET_ALL} {Fore.BLUE}{config.version}{Style.RESET_ALL}"
    )
    
@app.command()
def commands():
    """
    Lista os comandos disponíveis
    """
    typer.echo(f"{Fore.CYAN}Comandos disponíveis{Style.RESET_ALL}")
    for idx, command in enumerate(cmd.available_commands(), start=1):
        typer.echo(
            f"{Fore.YELLOW}{idx}{Style.RESET_ALL} - {Fore.GREEN}{command}{Style.RESET_ALL}"
        )
        
@app.command()
def exec(
    command: str = typer.Argument(..., help="Nome do comando"),
    arg: str = typer.Option(None, help="Nome do índice"),
    parallel: int = typer.Option(1, help="Número de processos paralelos"),
):
    """
    Executa um comando
    """
    try:
                
        if command not in cmd.available_commands():
            raise Exception(f"O comando {command} não existe")
        
        command = command.replace("-", "_")
        cmd.exec_command(command, arg, parallel=parallel)
        
    except Exception as e:
        app.logger.error(e)
        raise typer.Exit(code=config.exit_code.ERROR.value)