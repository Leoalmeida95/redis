import redis
import sys

key = 'produtos:'

def gera_id():
    try:
        conn = conectar()
        identificador = conn.get('chave')

        if identificador:
            identificador = conn.incr('chave')
            return identificador
        else:
            conn.set('chave', 1)
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
        utf8 = 'utf-8'
        ignore = 'ignore'

        if len(dados) > 0:
            print('Listando produtos...')
            print('....................')
            for identificador in dados:
                produto = conn.hgetall(identificador)
                print(f"Id: {str(identificador, utf8, ignore)}")
                print(f"Produto: {str(produto[b'nome'], utf8, ignore)}")
                print(f"Preço: {str(produto[b'preco'], utf8, ignore)}")
                print(f"Estoque: {str(produto[b'estoque'], utf8, ignore)}")
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
            print(f'O produto {nome} foi inserido com sucesso!')
        else:
            print('Não foi possível inserir o produto.')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inserir o produto. {e}')
        print('Inserindo novo produto...')
    print('....................')
    desconectar(conn)


def atualizar():
    conn = conectar()

    print('Atualizando um produto...')
    print('....................')

    num_id = input('Informe o número do identificador do produto:')

    identificador = f'{key}{num_id}'

    existe = conn.hkeys(identificador)

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

def deletar():
    conn = conectar()

    print('Deltando um produto...')
    print('....................')

    num_id = input('Informe o número do identificador do produto:')

    identificador = f'{key}{num_id}'

    existe = conn.hkeys(identificador)

    if existe:
        try:
            res = conn.delete(identificador)
            if res == 1:
                print(f'O produto foi deletado com sucesso!')
            else:
                print('Não foi possível deletar o produto.')
        except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível deletar o produto. {e}')
    else:
        print(f'Não há nenhum produto cadastrado com o identificador {identificador}.')
    desconectar(conn)

def menu():
    print('\n')
    print('======================Gerenciamento dos Produtos======================')
    print('Selecione uma opção:')
    print('1 - Listar produtos')
    print('2 - Inserir produto')
    print('3 - Atualizar produto')
    print('4 - Apagar produto')
    print('5 - Sair')
    print('\n')

    opcao = int(input())
    
    if opcao in [1,2,3,4,5]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        elif opcao == 5:
            sys.exit('================================ Fim ==============================')
    else:
        print('Digite uma opcao válida.')

    menu()