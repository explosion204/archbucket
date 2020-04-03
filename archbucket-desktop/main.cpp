#include "gui/mainwindow.h"
#include "gui/mainform.h"
#include <QApplication>

#ifdef __WIN32__
#include <winsock2.h>
#else
#include <sys/socket.h>
#endif

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainForm w;
    w.show();
    return a.exec();

}
