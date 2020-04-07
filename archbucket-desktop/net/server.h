#ifndef SERVER_H
#define SERVER_H

#ifdef _WIN32
    #ifndef _WIN32_WINNT
        #define _WIN32_WINNT 0x0501 // win XP
    #endif
    #include <winsock2.h>
    #include <ws2tcpip.h>
#else
    #include <sys/socket.h>
    #include <arpa/inet.h>
    #include <netdb.h> //getaddrinfo(), freeaddrinfo()
    #include <unistd.h> // close()
#endif

#include <QTcpSocket>
#include <QDataStream>
#include <QString>

class Server
{
private:
    QString ip;
    int port;
    bool is_busy;

public:
    Server(QString ip, int port);
    ~Server();
    QString getIp();
    int getPort();

    bool ping();
    QString getResponse(QString request);
};

#endif // SERVER_H
