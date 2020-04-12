#include "mainform.h"
#include "ui_mainform.h"

MainForm::MainForm(Updater *updater, QWidget *parent) :
    QWidget(parent),
    ui(new Ui::MainForm)
{
    ui->setupUi(this);
    this->updater = updater;
    connect(updater, &Updater::connection_broken, this, &MainForm::on_connectionBroken);
    updateInfo();
}

MainForm::~MainForm()
{
    delete ui;
}

void MainForm::on_connectionBroken()
{
    QMessageBox::warning(this, "Connection error", "Connection with server is broken.");
    close();
    (new LoginForm)->show();
}

void MainForm::updateInfo()
{
    ui->serverStatusLabel->setText(updater->getServerStatus());
    //ui->ipLabel->setText(updater->getIp());
    //ui->portLabel->setText(QString::number(updater->getPort()));
    ui->botStatusLabel->setText(updater->getBotStatus());
    //ui->pipelinesLabel->setText(updater->getPipelinesCount());
}
