
# Verificar se o ambiente virtual pipenv está ativo
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Erro: O ambiente virtual pipenv não está ativo."
  exit 1
fi

# Instalar o módulo build no ambiente virtual
pipenv install build

# Construir o pacote
python -m build .

# Desinstalar a versão anterior do pacote (se existir)
pip3 uninstall -y gspl

# Encontrar o arquivo Wheel mais recente
path_to_file=$(find dist -type f -name "*.whl" | sort -V | tail -n 1)

# Verificar se o arquivo Wheel foi encontrado
if [ -z "$path_to_file" ]; then
  echo "Erro: Nenhum arquivo Wheel encontrado na pasta dist."
  exit 1
fi

# Instalar o pacote mais recente
pip install --ignore-installed --no-cache-dir -U "$path_to_file"

# Verificar se a instalação foi bem-sucedida
if [ $? -ne 0 ]; then
  echo "Erro: Falha ao instalar o pacote."
  exit 1
fi

# Testar a importação do pacote
python -c "import gspl; print(gspl)"

# Testar o script console
question-console -h

# Limpar variáveis
unset path_to_file
