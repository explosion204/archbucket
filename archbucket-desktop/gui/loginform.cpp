#include "loginform.h"
#include "ui_loginform.h"

LoginForm::LoginForm(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::LoginForm)
{
    ui->setupUi(this);
}

LoginForm::~LoginForm()
{
    delete ui;
}

void LoginForm::on_connectButton_clicked()
{
    if (!ui->ipEdit->text().isEmpty() && !ui->portEdit->text().isEmpty())
    {
        if (Updater::getInstance()->connect(ui->ipEdit->text(), ui->portEdit->text().toInt()))
            QMessageBox::information(this, "Info", "Connected!");
        else
            QMessageBox::information(this, "Info", "Not connected.");
    }
}
