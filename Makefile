
# comandos para o dia a dia de desenvolvimento

# cores
RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m # No Color
YELLOW=\033[0;33m

# funação para criar o arquivo de env
define create_env
	@echo "${YELLOW}criando arquivo de env 🏂${NC}"
	@cat devtools/envs/dev.txt > .env
	@echo "${GREEN}Variaveis setadas! 👌${NC}"
endef


define clean
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@rm -f celerybeat-schedule.bak
	@rm -f celerybeat-schedule.dat
	@rm -f celerybeat-schedule.dir
	@rm -f celerybeat-schedule
	@rm -f celerybeat-schedule.db
endef


env:
	@clear
	$(call create_env)

clear:
	@clear
	$(call clean)

build:
	@clear
	@./scripts/build.sh

up:
	@clear
	@cd docker && docker-compose up -d

down:
	@clear
	@cd docker && docker-compose down

freeze:
	@clear
	@pipenv requirements --dev > devtools/requirements/dev.txt

