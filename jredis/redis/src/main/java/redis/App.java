package redis;

import java.util.Map;
import java.util.Scanner;
import java.util.Set;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.exceptions.JedisConnectionException;

public class App 
{

    private static String key = "produtos:*";

    public static Jedis conectar(){
        Jedis conn = new Jedis("localhost");

        return conn;
    }

    public static void desconectar(Jedis conn){

        conn.disconnect();
    }

    public static void listar(){
        Jedis conn = conectar();

        try{
            Set<String> res = conn.keys(key);

            if(res.size() >0){
                System.out.println("Listando os produtos...");
                System.out.println("-----------------------");

                for(String identificador: res){
                    Map<String, String> produto = conn.hgetAll(identificador);
                    System.out.println("Id: " + identificador);
                    System.out.println("Produto: " + produto.get("nome"));
                    System.out.println("Preço: " + produto.get("preco"));
                    System.out.println("Estoque: " + produto.get("estoque"));
                    System.out.println("-----------------------");
                }

            }else{
                System.out.println("Não existem produtos cadastrados.");
            }
        }
        catch(JedisConnectionException e){
            System.out.println("Verifique se o servidor Redis está ativo");
        }

        desconectar(conn);
    }

    public static void main( String[] args )
    {
        conectar();

        Scanner teclado = new Scanner(System.in);

        System.out.println("======================Gerenciamento dos Produtos======================");
        System.out.println("Selecione uma opção");
        System.out.println("1 - Listar os Produtos");

        int opcao = Integer.parseInt(teclado.nextLine());

        if(opcao == 1)
        {
            listar();
        }
        else{
            System.out.println("Escolha uma opção válida.");
        }

        

        System.out.println( "Redis is running on java application..." );
    }
}
