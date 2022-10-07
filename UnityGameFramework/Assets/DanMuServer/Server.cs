using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using UnityEngine;

public class Client
{
    public Socket socket;
    public byte[] readBuff = new byte[1024];

    public Client(Socket socket)
    {
        this.socket = socket;
    }
}

public class Server : MonoBehaviour
{
    public string ip;
    public int port;


    Socket serverSocket;

    Dictionary<Socket, Client> clients = new Dictionary<Socket, Client>();
    void Start()
    {
        startSocket();
    }

    private void startSocket()
    {
        serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        //Bind
        IPAddress ipAdress = IPAddress.Parse(ip);
        IPEndPoint ipEndPoint = new IPEndPoint(ipAdress, port);
        serverSocket.Bind(ipEndPoint);

        //Listen
        serverSocket.Listen(0);
        Debug.Log($"[Server] start,ip:{ip},port:{port}");

        //Accept
        serverSocket.BeginAccept(acceptCallback, serverSocket);

    }

    private void acceptCallback(IAsyncResult ar)
    {
        try
        {
            Socket s = (Socket)ar.AsyncState;
            Socket c = s.EndAccept(ar);
            Debug.LogError("[client] connected");
            Client client = new Client(c);
            clients[c] = client;
            c.BeginReceive(client.readBuff, 0, 1024, 0, receiveCallback, client);

        }
        catch (Exception ex)
        {

            Debug.LogError("server socket accept fail:" + ex.ToString());
        }
    }

    private void receiveCallback(IAsyncResult ar)
    {
        try
        {
            Client client = (Client)ar.AsyncState;
            Socket c = client.socket;
            int count = c.EndReceive(ar);
            if (count == 0)
            {
                c.Close();
                clients.Remove(c);
                Debug.LogError("[client] socket close");
                return;
            }

            string recvStr = System.Text.Encoding.UTF8.GetString(client.readBuff, 0, count);
            Debug.Log("[client]" + recvStr);
            //continue recv
            c.BeginReceive(client.readBuff, 0, 1024, 0, receiveCallback, client);
        }
        catch (Exception ex)
        {
            Client client = (Client)ar.AsyncState;
            clients.Remove(client.socket);
            client.socket.Close();
            Debug.LogError("receive fail:" + ex.ToString());
        }
    }
}
