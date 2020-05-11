package redis;

import java.nio.charset.Charset;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import static java.nio.charset.StandardCharsets.*;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.exceptions.JedisConnectionException;

public class App {

    private static String key = "produtos:";

    protected static Jedis conectar() {
        Jedis conn = new Jedis("localhost");

        return conn;
    }

    protected static void desconectar(Jedis conn) {

        conn.disconnect();
    }

    protected static String gerarChave() {

        Jedis conn = conectar();
        String identity = "chave";
        String initial = "1";

        try {
            String identificador = conn.get(identity);

            if (identificador != null){
                //converter string de bytes to UTF8
                return UTF_8.encode(conn.incr(identity).toString()).toString();
            }

            conn.set(identity, initial);

        } catch (JedisConnectionException e) {
            System.out.println("Verifique se o servidor Redis está ativo");
        }

        desconectar(conn);
        
        return initial;
    }

    protected static void listar() {
        Jedis conn = conectar();

        try {
            Set<String> res = conn.keys(key);

            if (res.size() > 0) {
                System.out.println("Listando os produtos...");
                System.out.println("-----------------------");

                for (String identificador : res) {
                    Map<String, String> produto = conn.hgetAll(identificador);
                    System.out.println("Id: " + identificador);
                    System.out.println("Produto: " + produto.get("nome"));
                    System.out.println("Preço: " + produto.get("preco"));
                    System.out.println("Estoque: " + produto.get("estoque"));
                    System.out.println("-----------------------");
                }

            } else {
                System.out.println("Não existem produtos cadastrados.");
            }
        } catch (JedisConnectionException e) {
            System.out.println("Verifique se o servidor Redis está ativo");
        }

        desconectar(conn);
    }

    protected static void inserir(Scanner teclado) {
        Jedis conn = conectar();

        try {

            System.out.println("Inserindo novo produto...");
            System.out.println("-----------------------");

            Map<String, String> produto = new HashMap<String, String>();
            produto.put("Id", key + gerarChave());
            System.out.println("Produto:");
            produto.put("nome", teclado.nextLine());
            System.out.println("Preço:");
            produto.put("preco", teclado.nextLine());
            System.out.println("Estoque:");
            produto.put("estoque", teclado.nextLine());

            String result = conn.hmset(key, produto);

            if (result != null)
                System.out.println("Novo produto criado com sucesso!");
            else
                System.out.println("Não foi possível inserir o novo produto");

            System.out.println("-----------------------");

        } catch (JedisConnectionException e) {
            System.out.println("Verifique se o servidor Redis está ativo");
        }

        desconectar(conn);
    }

    protected static void alterar(Scanner teclado) {
        Jedis conn = conectar();

        try {

            System.out.println("Alterando produto...");
            System.out.println("-----------------------");

            Map<String, String> produto = new HashMap<String, String>();
            System.out.println("Chave:");
            String identificador = teclado.nextLine();

            Set<String> existe = conn.hkeys(key+identificador);

            if(!existe.isEmpty()){   
                produto.put("Id",key+identificador);
                System.out.println("Produto:");
                produto.put("nome", teclado.nextLine());
                System.out.println("Preço:");
                produto.put("preco", teclado.nextLine());
                System.out.println("Estoque:");
                produto.put("estoque", teclado.nextLine());
                String result = conn.hmset(key, produto);
    
                if (result != null)
                    System.out.println("Produto alterado com sucesso!");
                else
                    System.out.println("Não foi possível alterar o produto");
    
                System.out.println("-----------------------");
            }
            else
                System.out.println("Não há produto registrado com essa chave.");

        } catch (JedisConnectionException e) {
            System.out.println("Verifique se o servidor Redis está ativo");
        }

        desconectar(conn);
    }

    protected static void menu(){
        Scanner teclado = new Scanner(System.in);

        System.out.println("======================Gerenciamento dos Produtos======================");
        System.out.println("Selecione uma opção");
        System.out.println("1 - Listar os Produtos");
        System.out.println("2 - Inserir novo Produto");
        System.out.println("3 - Alterar Produto");
        System.out.println("5 - Sair");

        int opcao = Integer.parseInt(teclado.nextLine());

        if (opcao == 1) 
            listar();
        else if(opcao == 2)
            inserir(teclado);
        else if(opcao == 3)
            alterar(teclado);
        else if(opcao == 5){
            System.out.println("================================Fim=================================");
            System.exit(0);
        }
         else 
            System.out.println("Escolha uma opção válida.");
        
            menu();
    }

    public static void main(String[] args) {
        conectar();
        menu();
    }
}
