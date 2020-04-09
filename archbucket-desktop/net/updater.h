#ifndef UPDATER_H
#define UPDATER_H

#include "net/server.h"
#include <thread>
#include <regex>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QMap>

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
    QMap<QString, bool> getModules();
    QMap<QString, bool> getApiModules();
    QString getLogs();

    //set functions
    bool startBot();
    bool stopBot();
    bool restartBot();
    bool importModule(QString name, QString source_code);
    bool removeModule(QString name);
    bool importApiModule(QString name, QString class_name, QString source_code);
    bool removeApiModule(QString name);

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
