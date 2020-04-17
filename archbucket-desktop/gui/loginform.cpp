#include "loginform.h"
#include "ui_loginform.h"

LoginForm::LoginForm(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::LoginForm)
{
    ui->setupUi(this);
    setFixedSize(338, 467);

    // loading animation
    loading_movie = new QMovie(":/gifs/assets/loading.gif");
    connect(loading_movie, &QMovie::frameChanged, this, &LoginForm::setButtonIcon);
    if (loading_movie->loopCount() != -1)
        connect(loading_movie, &QMovie::finished, loading_movie, &QMovie::start);

    connect(this, &LoginForm::connecting_ended, this, &LoginForm::on_connecting_ended);
}

LoginForm::~LoginForm()
{
    delete ui;
    delete loading_movie;
}

void LoginForm::on_connectButton_clicked()
{
    if (!ui->ipEdit->text().isEmpty() && !ui->portEdit->text().isEmpty())
    {
        std::regex ip_re(R"(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$)");
        std::regex port_re(R"(^\d{1,5}$)");
        if (std::regex_match(ui->ipEdit->text().toStdString(), ip_re) && std::regex_match(ui->portEdit->text().toStdString(), port_re))
        {
            ui->ipEdit->setReadOnly(true);
            ui->portEdit->setReadOnly(true);
            ui->connectButton->setText("");
            ui->connectButton->setEnabled(false);

            loading_movie->start();

            std::thread([this] ()
            {
                Updater *updater = new Updater(5);
                updater->establishConnection(ui->ipEdit->text(), ui->portEdit->text().toInt());
                connecting_ended(updater->isConnected(), updater);

                loading_movie->stop();
            }).detach();

        }
    }
}

void LoginForm::on_connecting_ended(bool result, Updater *updater)
{
    if (result)
    {
        close();
        (new MainForm(updater))->show();
        delete this;
    }
    else
    {
        QMessageBox::warning(this, "Connection error", "Cannot connect to server. Make sure typed address is correct.");
        ui->ipEdit->setReadOnly(false);
        ui->portEdit->setReadOnly(false);
        ui->connectButton->setText("Connect");
        ui->connectButton->setEnabled(true);
        ui->connectButton->setIcon(QIcon());
    }
}

void LoginForm::setButtonIcon(int frame)
{
    ui->connectButton->setIcon(QIcon(loading_movie->currentPixmap()));
}
