import redis

def gera_id():
    try:
        conn = conectar()
        chave = conn.get('chave')

        if chave:
            chave = conn.incr('chave')
            return chave
        else:
            conn.set('chave',1)
            return 1
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível gerar a chave: {e}')

def conectar():
    conn = redis.Redis(host='localhost', port=6379)

    return conn

def desconectar(conn):

    conn.connection_pool.disconnect()

def listar():
    conn = conectar()

    try:
        dados = conn.keys(pattern='produtos:*')

        if len(dados) > 0:
            print('Listando produtos...')
            print('....................')
            for chave in dados:
                produto = conn.hgetall(chave)
                print(f"Id: {str(chave, 'utf-8', 'ignore')}")
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

    nome = input('Informe o nome do produto:')
    preco = input('Informe o preco do produto:')
    estoque = input('Informe o estoque:')

    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    chave = f'produtos:{gera_id()}'

    try:
        res = conn.hmset(chave, produto)
        if res:
            print('O produto {nome} foi inserido com sucesso!')
        else:
            print('Não foi possível inserir o produto.')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inseror o produto. {e}')
    
    desconectar(conn)