import sqlite3
import os
from time import sleep
from uuid import uuid4

if not os.path.exists('database.db'):
  print('Banco de dados não encontrado!')
  print('Criando banco de dados...')
  import create_database
  sleep(0.5)

connection = sqlite3.connect('database.db', check_same_thread=False)

cursor = connection.cursor()

rodando = True

while rodando:
  print()
  print(' -= Painel de Administrador =-')
  print()
  print('  1. Criar usuário')
  print('  2. Listar usuários')
  print('  3. Deletar usuário')
  print('  4. Gerar chave novamente')
  print('  5. Listar transações')
  print('  6. Listar transações por ID de usuário')
  print('  7. Sair')
  print()

  try:
    entrada = int(input('  > '))
  except KeyboardInterrupt:
    entrada = 7
  except:
    print()
    print('  A entrada precisa ser um número!')
    sleep(0.5)
    continue
  
  print()

  if entrada == 1:
    username = input('  Digite o nome do usuário: ')
    new_key = str(uuid4())
    cursor.execute('INSERT INTO users (username, key) VALUES (?, ?)', (username, new_key))
    print()
    print(f'  Usuário {username} adicionado com sucesso! ID: {cursor.lastrowid}, Chave: {new_key}')
    connection.commit()
  elif entrada == 2:
    cursor.execute('SELECT id, username, key FROM users')
    users = cursor.fetchall()

    if users:
      for id, username, key in users:
        print(f'  {id}. {username} ({key})')
    else:
      print()
      print('  Nenhum usuário no momento!')
  elif entrada == 3:
    try:
      id = int(input('  Digite o ID do usuário: '))
    except:
      print()
      print('  A entrada precisa ser um número!')
      sleep(0.5)
      continue

    cursor.execute('SELECT id, username, key FROM users')
    users = cursor.fetchall()
    user = [_ for _ in users if _[0] == id]

    print()
    if user:
      cursor.execute('DELETE FROM users WHERE id = ?', (id,))
      print(f'  Usuário {user[0][1]} foi removido com sucesso!')
      connection.commit()
    else:
      print('  Este usuário não existe!')
  elif entrada == 4:
    try:
      id = int(input('  Digite o ID do usuário: '))
    except:
      print()
      print('  A entrada precisa ser um número!')
      sleep(0.5)
      continue

    cursor.execute('SELECT id, username, key FROM users')
    users = cursor.fetchall()
    user = [_ for _ in users if _[0] == id]

    print()
    if user:
      new_key = str(uuid4())
      cursor.execute('UPDATE users SET key = ? WHERE id = ?', (new_key, id))
      print(f'  A chave do usuário {user[0][1]} foi gerada novamente com sucesso! Chave: {new_key}')
      connection.commit()
    else:
      print('  Este usuário não existe!')
  elif entrada == 5:
    cursor.execute('SELECT t.id, t.id_user, u.username, t.prompt_tokens, t.completion_tokens, t.created_at FROM transactions t, users u WHERE t.id_user = u.id')
    transactions = cursor.fetchall()

    if transactions:
      print('  Date and Time / Prompt / Completion / Total / Username')
      for id, id_user, username, prompt_tokens, completion_tokens, created_at in transactions:
        print(f'  [{created_at}] / {prompt_tokens} / {completion_tokens} / {prompt_tokens + completion_tokens} / {username} ({id_user})')
    else:
      print()
      print('  Nenhuma transação no momento!')
  elif entrada == 6:
    try:
      id = int(input('  Digite o ID do usuário: '))
    except:
      print()
      print('  A entrada precisa ser um número!')
      sleep(0.5)
      continue

    cursor.execute('SELECT id, username, key FROM users')
    users = cursor.fetchall()
    user = [_ for _ in users if _[0] == id]

    print()
    if user:
      cursor.execute('SELECT t.id, t.id_user, u.username, t.prompt_tokens, t.completion_tokens, t.created_at FROM transactions t, users u WHERE t.id_user = u.id AND u.id = ?', (id, ))
      transactions = cursor.fetchall()

      if transactions:
        print('  Date and Time / Prompt / Completion / Total / Username')
        for id, id_user, username, prompt_tokens, completion_tokens, created_at in transactions:
          print(f'  [{created_at}] / {prompt_tokens} / {completion_tokens} / {prompt_tokens + completion_tokens} / {username} ({id_user})')
      else:
        print('  Nenhuma transação no momento!')
    else:
      print('  Este usuário não existe!')
    
  elif entrada == 7:
    rodando = False
  else:
    print()
    print('  Opção inválida!')
  
  sleep(0.5)