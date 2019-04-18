import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;


public class Main {

    public static void main(String[] args) {
        try{

            // 소켓 생성
            ServerSocket serverSocket = new ServerSocket(0);
            System.out.println("Local Port: " + serverSocket.getLocalPort());

            // 소켓 연결
            Socket socket = serverSocket.accept();
            System.out.println("from Address is " +
                socket.getInetAddress() + ":" + socket.getPort());

            // 데이터 전송
            OutputStream outputStream = socket.getOutputStream();
            PrintStream printStream = new PrintStream(outputStream);
            printStream.print("Server send data. ");
            printStream.close();

            // 소켓 해제
            socket.close();
        }catch(IOException e){
            System.out.println(e.toString());
        }
    }
}
