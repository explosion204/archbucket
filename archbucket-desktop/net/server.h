#ifndef SERVER_H
#define SERVER_H

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
