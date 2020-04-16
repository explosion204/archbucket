#ifndef UPDATER_H
#define UPDATER_H

#include "net/server.h"
#include <thread>
#include <regex>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QMap>

struct ServerData
{
    QString server_status;
    QString bot_status;
    QString pipelines_count;
    QMap<QString, bool> modules;
    QMap<QString, bool> api_modules;
    QString logs;
};

class Updater : public QObject
{
    Q_OBJECT
private:
    int interval;
    bool is_connected;
    Server *server;
public:
    ServerData data;

    Updater(int seconds);
    void establishConnection(QString ip, int port);
    bool isConnected();
    QString getIp();
    int getPort();

    //get all data from server
    void getAllData();

    //get functions
    QString getServerStatus();
    QString getBotStatus();
    QString getPipelinesCount();
    QMap<QString, bool> getModules();
    QMap<QString, bool> getApiModules();
    QString getLogs();

    //set functions
    QPair<bool, QString> startBot();
    QPair<bool, QString> stopBot();
    QPair<bool, QString> restartBot();
    QPair<bool, QString> importModule(QString name, QString source_code);
    QPair<bool, QString> removeModule(QString name);
    QPair<bool, QString> importApiModule(QString name, QString class_name, QString source_code);
    QPair<bool, QString> removeApiModule(QString name);

    QPair<bool, QString> setModuleStatus(QString name, bool status);
    QPair<bool, QString> setApiModuleStatus(QString name, bool status);

signals:
    void connection_broken();
    void data_updated();
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
