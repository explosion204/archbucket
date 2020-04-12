#include "loginform.h"
#include "ui_loginform.h"

LoginForm::LoginForm(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::LoginForm)
{
    ui->setupUi(this);
    setFixedSize(338, 467);
}

LoginForm::~LoginForm()
{
    delete ui;
}

void LoginForm::on_connectButton_clicked()
{
    if (!ui->ipEdit->text().isEmpty() && !ui->portEdit->text().isEmpty())
    {
        Updater *updater = new Updater(5);
        std::regex ip_re(R"(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$)");
        std::regex port_re(R"(^\d{1,5}$)");
        if (std::regex_match(ui->ipEdit->text().toStdString(), ip_re) && std::regex_match(ui->portEdit->text().toStdString(), port_re))
        {
            updater->establishConnection(ui->ipEdit->text(), ui->portEdit->text().toInt());
            if (updater->isConnected())
            {
                close();
                (new MainForm(updater))->show();
            }
            else
            {
                QMessageBox::warning(this, "Connection error", "Cannot connect to server. Make sure typed address is correct.");
            }
        }
    }
}
