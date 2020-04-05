#include "gui/mainform.h"
#include <QApplication>

#include <net/server.h>

int main(int argc, char *argv[])
{
//    QApplication a(argc, argv);
//    MainForm w;
//    w.show();
//    return a.exec();

    auto server = Server();
    server.setIp("192.168.100.31");
    server.setPort(52205);
    QString response = server.getResponse("get modules");
    qDebug() << response;
    return 0;
}
