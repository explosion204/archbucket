#include "connection.h"

Connection::Connection(QString ip, int port) : server(ip, port)
{
    if (server.ping())
    {
        is_available = true;
        auto ping_func = [this] ()
        {
            while (true)
            {
                if (server.ping())
                {
                    is_available = false;
                    break;
                }
                std::this_thread::sleep_for(std::chrono::seconds(5));
            }
        };
        std::thread ping_thread(ping_func);
        ping_thread.detach();
    }
    else
        is_available = false;
}

QString Connection::getIp()
{
    if (is_available)
        return server.getIp();
    throw ConnectionException();
}

int Connection::getPort()
{
    if (is_available)
        return server.getPort();
    throw ConnectionException();
}

QString Connection::getResponse(QString request)
{
    if (is_available)
        return server.getResponse(request);
    throw ConnectionException();
}

bool Connection::isAvailable()
{
    return is_available;
}
