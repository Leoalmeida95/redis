import redis

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