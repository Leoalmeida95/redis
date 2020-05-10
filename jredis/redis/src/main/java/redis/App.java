package redis;

import java.util.Scanner;
import redis.clients.jedis.Jedis;

public class App 
{
    public static Jedis conectar(){
        Jedis conn = new Jedis("localhost");

        return conn;
    }

    public static void main( String[] args )
    {
        conectar();
        System.out.println( "Redis is running on java application..." );
    }
}
