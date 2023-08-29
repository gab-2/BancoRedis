import redis

conexao_redis = redis.Redis(host='localhost', port=6379)

def adicionar_tarefa(conexao_redis, descricao):
    tarefa_id = conexao_redis.incr('contador_tarefas')  
    tarefa_key = f'tarefa:{tarefa_id}'
    conexao_redis.set(tarefa_key, descricao)
    conexao_redis.rpush('tarefas', tarefa_id)

def listar_tarefas(conexao_redis):
    tarefas_ids = conexao_redis.lrange('tarefas', 0, -1)
    for tarefa_id in tarefas_ids:
        tarefa_key = f'tarefa:{tarefa_id.decode("utf-8")}'
        descricao_bytes = conexao_redis.get(tarefa_key)

        if descricao_bytes is not None:
            descricao = descricao_bytes.decode('utf-8')
            print(f"ID: {tarefa_id.decode('utf-8')}, Descrição: {descricao}")
        else:
            print(f"ID: {tarefa_id.decode('utf-8')}, Descrição não encontrada")

def remover_tarefa(conexao_redis, tarefa_id):
    tarefa_key = f'tarefa:{tarefa_id}'
    conexao_redis.lrem('tarefas', 0, tarefa_id)
    conexao_redis.delete(tarefa_key)

while True:
    print("\n1. Adicionar Tarefa\n2. Listar Tarefas\n3. Remover Tarefa\n4. Sair")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        descricao_tarefa = input("Digite a descrição da tarefa: ")
        adicionar_tarefa(conexao_redis, descricao_tarefa)
        print("Tarefa adicionada com sucesso!")

    elif escolha == '2':
        listar_tarefas(conexao_redis)

    elif escolha == '3':
        tarefa_id = input("Digite o ID da tarefa que deseja remover: ")
        remover_tarefa(conexao_redis, tarefa_id)
        print("Tarefa removida com sucesso!")

    elif escolha == '4':
        print("Saindo do programa!")
        break

    else:
        print("Opção inválida. Tente novamente.")