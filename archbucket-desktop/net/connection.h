#ifndef CONNECTION_H
#define CONNECTION_H

#include "net/server.h"
#include <QString>
#include <QObject>
#include <thread>

class Connection : public QObject
{
    Q_OBJECT
private:
    Server server;
    bool is_available;

public:
    Connection(QString ip, int port);

    QString getIp();
    int getPort();
    bool isAvailable();

    QString getResponse(QString request);

signals:
    void connection_broken();
};

class ConnectionException : public std::exception
{
public:
    const char* what() const noexcept override
    {
        return "Connection is not available.";
    }
};

#endif // CONNECTION_H
