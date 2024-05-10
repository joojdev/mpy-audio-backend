import sqlite3
import os

if not os.path.exists('database.db'):
  import create_database

# Conectando ao banco de dados SQLite
connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

def create_transaction(user_id, prompt_tokens, completion_tokens):
  """
  Insere uma nova transação no banco de dados com a data e hora atual automaticamente.

  Args:
  user_id (int): ID do usuário que está realizando a transação.
  prompt_tokens (int): Número de tokens utilizados no prompt.
  completion_tokens (int): Número de tokens utilizados na completção.

  Returns:
  bool: True se a transação foi criada com sucesso, False caso contrário.
  """
  try:
    cursor.execute('''
    INSERT INTO transactions (id_user, prompt_tokens, completion_tokens)
    VALUES (?, ?, ?)
    ''', (user_id, prompt_tokens, completion_tokens))
    connection.commit()
    return True
  except sqlite3.Error as e:
    print(f"Erro ao inserir a transação: {e}")
    return False
  
def search_user(key):
  """
  Busca o ID do usuário baseado na key fornecida.

  Args:
  key (str): Chave única do usuário.

  Returns:
  int: ID do usuário, ou None se não encontrado.
  """
  cursor.execute('''
  SELECT id FROM users WHERE key = ?
  ''', (key,))
  result = cursor.fetchone()
  if result:
    return result[0]
  else:
    return None