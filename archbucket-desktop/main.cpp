#include "gui/loginform.h"
#include <QApplication>

#include <net/server.h>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    LoginForm login_form;
    login_form.show();
    return a.exec();
}
