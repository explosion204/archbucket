#include "server.h"

Server::Server()
{

}

QString Server::getResponse(QString request)
{
//    QTcpSocket socket;

//    socket.connectToHost(ip, port);
//    if (socket.waitForConnected(1000))
//    {
//        socket.write(request.toUtf8());
//        socket.waitForReadyRead(5000);

//        auto buf = socket.readLine(1024);
//        return QString::fromUtf8(buf);
//    }
//    else
//    {
//        // error handling
//        return QString();
//    }
    WSADATA wsa_data;
    WSAStartup(MAKEWORD(1, 1), &wsa_data);
    SOCKET sock;
    SOCKADDR_IN server_addr;
    sock = socket(AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = inet_addr(ip.toLocal8Bit().data());
    connect(sock, (SOCKADDR*)&server_addr, sizeof(server_addr));
    send(sock, request.toLocal8Bit().data(), strlen(request.toLocal8Bit().data()), 0);
    shutdown(sock, SD_SEND);
    char recvbuf[1024];
    recv(sock, recvbuf, 1024, 0);
    return QString(recvbuf);
}

void Server::setIp(QString ip)
{
    this->ip = ip;
}

void Server::setPort(int port)
{
    this->port = port;
}

QString Server::getIp()
{
    return ip;
}

int Server::getPort()
{
    return port;
}
