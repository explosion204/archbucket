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
    // status
    ui->serverStatusLabel->setText(updater->getServerStatus());
    ui->ipLabel->setText(updater->getIp());
    ui->portLabel->setText(QString::number(updater->getPort()));
    ui->botStatusLabel->setText(updater->getBotStatus());
    ui->pipelinesLabel->setText(updater->getPipelinesCount());

    // modules
    auto api_list = updater->getApiModules();
    auto modules_list = updater->getModules();

    ui->apiList->clear();
    ui->modulesList->clear();

    int i = 0;
    for (auto api_name : api_list.keys())
    {
        ui->apiList->addItem(api_name);
        if (api_list[api_name])
            ui->apiList->item(i)->setCheckState(Qt::CheckState::Checked);
        else
            ui->apiList->item(i)->setCheckState(Qt::CheckState::Unchecked);
        i++;
    }

    i = 0;
    for (auto module_name : modules_list.keys())
    {
        ui->modulesList->addItem(module_name);
        if (modules_list[module_name])
            ui->modulesList->item(i)->setCheckState(Qt::CheckState::Checked);
        else
            ui->modulesList->item(i)->setCheckState(Qt::CheckState::Unchecked);
        i++;
    }
}
