#include "updater.h"

Updater* Updater::instance = nullptr;

Updater::Updater()
{
    curr_connection = nullptr;
}

Updater* Updater::getInstance()
{
    if (instance == nullptr)
    {
        instance = new Updater();
    }
    return instance;
}

bool Updater::connect(QString ip, int port)
{
    curr_connection = new Connection(ip, port);
    return curr_connection->isAvailable();
}
