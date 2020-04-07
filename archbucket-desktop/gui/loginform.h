#ifndef LOGINFORM_H
#define LOGINFORM_H

#include <QWidget>
#include <QMessageBox>

#include "net/updater.h"

namespace Ui {
class LoginForm;
}

class LoginForm : public QWidget
{
    Q_OBJECT

public:
    explicit LoginForm(QWidget *parent = nullptr);
    ~LoginForm();

private slots:
    void on_connectButton_clicked();

private:
    Ui::LoginForm *ui;
};

#endif // LOGINFORM_H
