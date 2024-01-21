from pydantic import BaseModel, Field
from threading import Thread

        
class BaseCommand(BaseModel):
    name: str = Field(default=f"{__name__}", description="Nome do comando")
    parallel: int = Field(default=1, description="Número de processos paralelos")

    class Config:
        arbitrary_types_allowed = True
        
    def execute(self):
        raise NotImplementedError("O método execute deve ser implementado")
            
    def _configure(self):
        pass
    
    def _execute(self):
        # executa o metodo execute em paralelo ou não
        if self.parallel > 1:
            threads = []
            for _ in range(self.parallel):
                threads.append(Thread(target=self.execute))
                threads[-1].start()
                
            for thread in threads:
                thread.join()
                
        else:
            self.execute()