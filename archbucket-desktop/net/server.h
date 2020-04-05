#ifndef SERVER_H
#define SERVER_H

#ifdef __WIN32__
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <sys/socket.h>
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
    Server();
    QString getIp();
    void setIp(QString ip);
    int getPort();
    void setPort(int port);

    bool isBusy();
    bool ping();
    QString getResponse(QString request);
};

#endif // SERVER_H
