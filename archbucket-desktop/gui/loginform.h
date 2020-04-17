#ifndef LOGINFORM_H
#define LOGINFORM_H

#include <QWidget>
#include <QMessageBox>
#include <QMovie>
#include <QDir>
#include <regex>

#include "net/updater.h"
#include "gui/mainform.h"

namespace Ui {
class LoginForm;
}

class LoginForm : public QWidget
{
    Q_OBJECT

public:
    explicit LoginForm(QWidget *parent = nullptr);
    ~LoginForm();

signals:
    void connecting_ended(bool result, Updater *updater);

private slots:
    void on_connectButton_clicked();
    void setButtonIcon();

    void on_connecting_ended(bool result, Updater *updater);

private:
    Ui::LoginForm *ui;
    QMovie *loading_movie;
};

#endif // LOGINFORM_H
