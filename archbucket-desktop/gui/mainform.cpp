#include "mainform.h"
#include "ui_mainform.h"

MainForm::MainForm(Updater *updater, QWidget *parent) :
    QWidget(parent),
    ui(new Ui::MainForm)
{
    ui->setupUi(this);
    this->updater = updater;
    connect(updater, &Updater::connection_broken, this, &MainForm::on_connection_broken);
    connect(updater, &Updater::data_updated, this, &MainForm::updateInfo);
    updateInfo();
}

MainForm::~MainForm()
{
    delete ui;
}

void MainForm::on_connection_broken()
{
    QMessageBox::warning(this, "Connection error", "Connection with server is broken.");
    close();
    (new LoginForm)->show();
}

void MainForm::updateInfo()
{
    // status
    ui->serverStatusLabel->setText(updater->data.server_status);
    ui->ipLabel->setText(updater->getIp());
    ui->portLabel->setText(QString::number(updater->getPort()));
    ui->botStatusLabel->setText(updater->data.bot_status);
    ui->pipelinesLabel->setText(updater->data.pipelines_count);

    // modules
    auto api_list = updater->data.api_modules;
    auto modules_list = updater->data.modules;

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

void MainForm::on_startBotButton_clicked()
{

}
