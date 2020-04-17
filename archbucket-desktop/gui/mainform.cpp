#include "mainform.h"
#include "ui_mainform.h"

MainForm::MainForm(Updater *updater, QWidget *parent) :
    QWidget(parent),
    ui(new Ui::MainForm)
{
    ui->setupUi(this);
    this->updater = updater;
    connect(updater, &Updater::connection_broken, this, &MainForm::on_connection_broken);
    connect(updater, &Updater::data_updated, this, &MainForm::updateStatus);
    updateStatus();
    updateListWidgets();
}

MainForm::~MainForm()
{
    delete ui;
    delete updater;
}

void MainForm::on_connection_broken()
{
    QMessageBox::warning(this, "Connection error", "Connection to server is broken.");
    close();
    (new LoginForm)->show();
    delete this;
}

void MainForm::updateStatus()
{
    ui->serverStatusLabel->setText(updater->data.server_status);
    ui->ipLabel->setText(updater->getIp());
    ui->portLabel->setText(QString::number(updater->getPort()));
    ui->botStatusLabel->setText(updater->data.bot_status);
    ui->pipelinesLabel->setText(updater->data.pipelines_count);

}

void MainForm::updateListWidgets()
{
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

void MainForm::on_apiList_itemChanged(QListWidgetItem *item)
{
    if (item->checkState() == Qt::Checked)
        updater->setApiModuleStatus(item->text(), true);
    else
        updater->setApiModuleStatus(item->text(), false);
}

void MainForm::on_modulesList_itemChanged(QListWidgetItem *item)
{
    if (item->checkState() == Qt::Checked)
        updater->setModuleStatus(item->text(), true);
    else
        updater->setModuleStatus(item->text(), false);
}

void MainForm::on_refreshApiListButton_clicked()
{
    auto api_list = updater->data.api_modules;

    ui->apiList->clear();

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
}

void MainForm::on_refreshModuleList_clicked()
{
    auto modules_list = updater->data.modules;

    ui->modulesList->clear();

    int i = 0;
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
    auto response = updater->startBot();
    if (!response.first)
    {
        QMessageBox::warning(this, "Error", response.second);
    }
    else
    {
        QMessageBox::information(this, "Info", response.second);
        ui->botStatusLabel->setText("running");
    }
}

void MainForm::on_stopBotButton_clicked()
{
    auto response = updater->stopBot();
    if (!response.first)
    {
        QMessageBox::warning(this, "Error", response.second);
    }
    else
    {
        QMessageBox::information(this, "Info", response.second);
        ui->botStatusLabel->setText("not running");
    }
}

void MainForm::on_restartBptButton_clicked()
{
    auto response = updater->restartBot();
    if (!response.first)
    {
        QMessageBox::warning(this, "Error", response.second);
    }
    else
    {
        QMessageBox::information(this, "Info", response.second);
    }
}

void MainForm::on_importApiButton_clicked()
{

}
