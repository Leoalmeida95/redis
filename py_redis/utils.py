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