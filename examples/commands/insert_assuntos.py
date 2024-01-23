import time
from gspl.console.app import app
from gspl.console.commands.command import BaseCommand

logger = BaseCommand.logger

class Command(BaseCommand):
        
    def execute(self):
        try:
            self.logger.info("Teste")
            self.logger.info("Teste2")
            # index_name = 'teste'
            # index_body = {
            # 'settings': {
            #     'index': {
            #         'number_of_shards': 4
            #     }
            # }
            # }
            # self.open_elastic.indices.create(
            #     index_name, body=index_body
            # )
        except Exception as e:
            self.logger.error(e)
            raise e
        
