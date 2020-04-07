#ifndef UPDATER_H
#define UPDATER_H

#include "net/server.h"
#include <thread>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QList>

class Updater : public QObject
{
    Q_OBJECT
private:
    int interval;
    bool is_connected;
    Server *server;
public:
    Updater(int seconds);
    void establishConnection(QString ip, int port);
    bool isConnected();
    QString getIp();
    int getPort();

    //get functions
    QString getServerStatus();
    QString getBotStatus();
    QString getPipelinesCount();
    QList<QString> getModules();
    QList<QString> getApiModules();
    QString getLogs();

    //set functions
    void startBot();
    void stopBot();
    void restartBot();
    void importModule(QString name, QString source_code);
    void removeModule(QString name);
    void importApiModule(QString name, QString class_name, QString source_code);
    void removeApiModule(QString name);

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

#endif // UPDATER_H
