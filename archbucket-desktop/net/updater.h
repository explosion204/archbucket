#ifndef UPDATER_H
#define UPDATER_H

#include "net/connection.h"

class Updater
{
private:
    static Updater *instance;

    Connection *curr_connection;

    Updater();
public:
    static Updater* getInstance();
    bool connect(QString ip, int port);
};

#endif // UPDATER_H
