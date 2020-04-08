#include "updater.h"

Updater::Updater(int seconds)
{
    interval = seconds;
    is_connected = false;
}

void Updater::establishConnection(QString ip, int port)
{
    server = new Server(ip, port);
    if (server->ping())
    {
        is_connected = true;
        auto ping_func = [this] ()
        {
            while (true)
            {
                if (!server->ping())
                {
                    is_connected = false;
                    connection_broken();
                    break;
                }
                std::this_thread::sleep_for(std::chrono::seconds(interval));
            }
        };
        std::thread ping_thread(ping_func);
        ping_thread.detach();
    }
}

bool Updater::isConnected()
{
    return is_connected;
}

QString Updater::getIp()
{
    return server->getIp();
}

int Updater::getPort()
{
    return server->getPort();
}

QString Updater::getServerStatus()
{
    if (is_connected)
    {
        QString response = server->getResponse("server status");
        if (response.isEmpty())
        {
            connection_broken();
            throw ConnectionException();
        }

        QJsonDocument json_doc = QJsonDocument::fromJson(response.toUtf8());
        QJsonObject json_obj = json_doc.object();
        std::string message = json_obj["message"].toString().toStdString();

        std::regex reg_expr(R"(^.*(local|global).*$)");
        std::smatch match;
        std::regex_match(message, match, reg_expr);

        return QString::fromStdString(match[1]);
    }
    throw ConnectionException();
}

QString Updater::getBotStatus()
{
    if (is_connected)
    {
        QString response = server->getResponse("bot status");
        if (response.isEmpty())
        {
            connection_broken();
            throw ConnectionException();
        }

        QJsonDocument json_doc = QJsonDocument::fromJson(response.toUtf8());
        QJsonObject json_obj = json_doc.object();

        if (json_obj["status"].toBool())
            return "running";
        else
            return "not running";
    }
    throw ConnectionException();
}

QString Updater::getPipelinesCount()
{
    if (is_connected)
    {
        QString response = server->getResponse("get pipelines");
        if (response.isEmpty())
        {
            connection_broken();
        }

        QJsonDocument json_doc = QJsonDocument::fromJson(response.toUtf8());
        QJsonObject json_obj = json_doc.object();

        return json_obj["message"].toString();
    }
    throw ConnectionException();
}
