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
                if (server->ping())
                {
                    is_connected = false;
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

QString Updater::getBotStatus()
{
    if (is_connected)
    {
        QString response = server->getResponse("bot status");
        QJsonDocument json_doc = QJsonDocument::fromJson(response.toUtf8());
        QJsonObject json_obj = json_doc.object();
        if (json_obj["status"].toBool())
            return "running";
        else
            return "not running";
    }
    throw ConnectionException();
}
