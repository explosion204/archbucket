#include "server.h"

Server::Server(QString ip, int port)
{
    this->ip = ip;
    this->port = port;
    is_busy = false;

    #ifdef _WIN32
        WSADATA wsa_data;
        WSAStartup(MAKEWORD(1, 1), &wsa_data);
    #endif
}

Server::~Server()
{
    #ifdef _WIN32
        WSACleanup();
    #endif
}

QString Server::getResponse(QString request)
{
    while (true)
    {
        if (!is_busy)
        {
            is_busy = true;
            SOCKET sock;
            SOCKADDR_IN server_addr;

            sock = socket(AF_INET, SOCK_STREAM, 0);
            server_addr.sin_family = AF_INET;
            server_addr.sin_port = htons(port);

            #ifdef _WIN32
                server_addr.sin_addr.s_addr = inet_addr(ip.toLocal8Bit().data());
            #else
                inet_pton(AF_INET, ip.toLocal8Bit().data(), &server_addr.sin_addr);
            #endif

            connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr));
            send(sock, request.toLocal8Bit().data(), strlen(request.toLocal8Bit().data()), 0);
            #ifdef _WIN32
                shutdown(sock, SD_SEND);
            #else
                shutdown(sock, SHUT_WR);
            #endif

            QString response;
            int bytes;
            char recvbuf[1024];
            do
            {
                bytes = recv(sock, recvbuf, 1024, 0);
                if (bytes > 0)
                    response.append(recvbuf);
            }
            while (bytes > 0);

            #ifdef _WIN32
                shutdown(sock, SD_RECEIVE);
                closesocket(sock);
            #else
                shutdown(sock, SD_RD);
                close(sock);
            #endif

            is_busy = false;
            return response;
        }
    }
}

bool Server::ping()
{
    return !getResponse("ping").isEmpty();
}

QString Server::getIp()
{
    return ip;
}

int Server::getPort()
{
    return port;
}
