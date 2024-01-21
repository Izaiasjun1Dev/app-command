import time
from gspl.console.app import app
from gspl.console.commands.command import BaseCommand


class Command(BaseCommand):
     
    def execute(self):
        app.logger.info("Executando o comando")
        self.get_data()
        self.processa_dados()
        app.logger.info("Comando executado")
        
    def get_data(self):
        app.logger.info("Obtendo os dados")
        
       
    def processa_dados(self):
        app.logger.info("Processando os dados")
        