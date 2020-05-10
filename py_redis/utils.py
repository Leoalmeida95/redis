import redis

key = 'produtos:'

def gera_id():
    try:
        conn = conectar()
        identificador = conn.get('chave')

        if identificador:
            identificador = conn.incr('chave')
            return identificador
        else:
            conn.set('chave',1)
            return 1
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível gerar o identificador: {e}')

def conectar():
    conn = redis.Redis(host='localhost', port=6379)

    return conn

def desconectar(conn):

    conn.connection_pool.disconnect()

def listar():
    conn = conectar()

    try:
        dados = conn.keys(pattern=f'{key}*')

        if len(dados) > 0:
            print('Listando produtos...')
            print('....................')
            for identificador in dados:
                produto = conn.hgetall(identificador)
                print(f"Id: {str(identificador, 'utf-8', 'ignore')}")
                print(f"Produto: {str(produto[b'nome'], 'utf-8', 'ignore')}")
                print(f"Preço: {str(produto[b'preco'], 'utf-8', 'ignore')}")
                print(f"Estoque: {str(produto[b'estoque'], 'utf-8', 'ignore')}")
                print('....................')
        else:
            print('Não foram encontrados produtos')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível listar os produtos. {e}')

    desconectar(conn)

def inserir():
    conn = conectar()

    print('Inserindo novo produto...')
    print('....................')

    nome = input('Informe o nome do produto:')
    preco = float(input('Informe o preco do produto:'))
    estoque = int(input('Informe o estoque:'))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    identificador = f'{key}{gera_id()}'

    try:
        res = conn.hmset(identificador, produto)
        if res:
            print('O produto {nome} foi inserido com sucesso!')
        else:
            print('Não foi possível inserir o produto.')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inserir o produto. {e}')
        print('Inserindo novo produto...')
    print('....................')
    desconectar(conn)


def atualizar():
    conn = conectar()

    print('Atualizando produto...')
    print('....................')

    identificador = input('Informe o identificador do produto:')

    existe = conn.hkeys(f'{key}{identificador}')

    if existe:
        nome = input('Informe o nome do produto:')
        preco = float(input('Informe o preco do produto:'))
        estoque = int(input('Informe o estoque:'))

        produto = {"nome": nome, "preco": preco, "estoque": estoque}

        try:
            res = conn.hmset(identificador, produto)
            if res:
                print(f'O produto {nome} foi atualizado com sucesso!')
            else:
                print('Não foi possível atualizar o produto.')
        except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível atualizar o produto. {e}')
    else:
        print(f'Não há nenhum produto cadastrado com o identificador {identificador}.')
    
    desconectar(conn)