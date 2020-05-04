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
    on_refreshLogsButton_clicked();

    // loading animation
    loading_movie = new QMovie(":/gifs/assets/loading.gif");
    loading_button = nullptr;
}

MainForm::~MainForm()
{
    delete ui;
    delete updater;
    delete loading_movie;
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

void MainForm::on_refreshModuleListButton_clicked()
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
    loading_button = ui->startBotButton;
    setLoadingButtonState(true);
    // block buttons
    setControlsState(false);

    connect(this, &MainForm::display_message, this, [this] (bool type, QString message)
    {
        setLoadingButtonState(false);
        on_display_message(type, message);
        disconnect();
    });

    std::thread([this]
    {
       auto response = updater->startBot();
       display_message(response.first, response.second);
    }).detach();

}

void MainForm::on_stopBotButton_clicked()
{
    loading_button = ui->stopBotButton;
    setLoadingButtonState(true);
    // block buttons
    setControlsState(false);

    connect(this, &MainForm::display_message, this, [this] (bool type, QString message)
    {
        setLoadingButtonState(false);
        on_display_message(type, message);
        disconnect();
    });

    std::thread([this]
    {
       auto response = updater->stopBot();
       display_message(response.first, response.second);
    }).detach();
}

void MainForm::on_restartBotButton_clicked()
{
    loading_button = ui->restartBotButton;
    setLoadingButtonState(true);
    // block buttons
    setControlsState(false);

    connect(this, &MainForm::display_message, this, [this] (bool type, QString message)
    {
        setLoadingButtonState(false);
        on_display_message(type, message);
        disconnect();
    });

    std::thread([this]
    {
       auto response = updater->restartBot();
       display_message(response.first, response.second);
    }).detach();
}

void MainForm::on_importApiButton_clicked()
{
    ImportApiForm *form = new ImportApiForm(updater, this);
    form->setModal(true);
    form->show();
}

void MainForm::on_importModuleButton_clicked()
{
    ImportModuleForm *form = new ImportModuleForm(updater, this);
    form->setModal(true);
    form->show();
}

void MainForm::on_removeApiButton_clicked()
{
    if (ui->apiList->currentRow() != -1)
    {
        int choice = QMessageBox::warning(this, "Warning", "Delete this api module?", QMessageBox::Yes, QMessageBox::Cancel);
        switch (choice)
        {
            case QMessageBox::Yes:
            {
                loading_button = ui->removeApiButton;
                setLoadingButtonState(true);
                // block buttons
                setControlsState(false);

                connect(this, &MainForm::display_message, this, [this] (bool type, QString message)
                {
                    setLoadingButtonState(false);
                    on_display_message(type, message);
                    disconnect();
                });
                connect(this, &MainForm::item_removed, this, &MainForm::on_item_removed);

                std::thread([this] ()
                {
                    auto response = updater->removeApiModule(ui->apiList->currentItem()->text());

                    if (response.first)
                        item_removed(ui->apiList, ui->apiList->currentRow());

                    display_message(response.first, response.second);
                }).detach();

                break;
            }
            case QMessageBox::No:
                break;
        }
    }
}

void MainForm::on_removeModuleButton_clicked()
{
    if (ui->modulesList->currentRow() != -1)
    {
        int choice = QMessageBox::warning(this, "Warning", "Delete this module?", QMessageBox::Yes, QMessageBox::Cancel);
        switch (choice)
        {
            case QMessageBox::Yes:
            {
                loading_button = ui->removeModuleButton;
                setLoadingButtonState(true);
                // block buttons
                setControlsState(false);

                connect(this, &MainForm::display_message, this, [this] (bool type, QString message)
                {
                    setLoadingButtonState(false);
                    on_display_message(type, message);
                    disconnect();
                });
                connect(this, &MainForm::item_removed, this, &MainForm::on_item_removed);

                std::thread([this] ()
                {
                    auto response = updater->removeModule(ui->modulesList->currentItem()->text());

                    if (response.first)
                        item_removed(ui->modulesList, ui->modulesList->currentRow());

                    display_message(response.first, response.second);
                }).detach();

                break;
            }
            case QMessageBox::No:
                break;
        }
    }
}

void MainForm::setLoadingButtonState(bool state)
{
    if (loading_button != nullptr)
    {
        if (state)
        {
            connect(loading_movie, &QMovie::frameChanged, this, [this] ()
            {
               loading_button->setIcon(QIcon(loading_movie->currentPixmap()));
            }
            );
            if (loading_movie->loopCount() != -1)
                connect(loading_movie, &QMovie::finished, loading_movie, &QMovie::start);

            loading_button->setEnabled(false);
            loading_movie->start();
        }
        else
        {
            loading_movie->stop();
            loading_button->setIcon(QIcon());
            loading_button->setEnabled(true);
        }
    }
}

void MainForm::on_display_message(bool type, QString message)
{
    QString title = type ? "Info" : "Error";
    QMessageBox::warning(this, title, message);

    //unblock buttons
    setControlsState(true);
}

void MainForm::on_item_removed(QListWidget *list_widget, int item_row)
{
    list_widget->takeItem(item_row);
}

void MainForm::setControlsState(bool state)
{
    ui->apiList->setEnabled(state);
    ui->modulesList->setEnabled(state);

    ui->startBotButton->setEnabled(state);
    ui->stopBotButton->setEnabled(state);
    ui->restartBotButton->setEnabled(state);
    ui->importApiButton->setEnabled(state);
    ui->importModuleButton->setEnabled(state);
    ui->removeApiButton->setEnabled(state);
    ui->removeModuleButton->setEnabled(state);
    ui->refreshApiListButton->setEnabled(state);
    ui->refreshModuleListButton->setEnabled(state);

    // except loading button
    if (state)
        loading_button->setEnabled(true);
    else
        loading_button->setEnabled(false);
}

void MainForm::on_refreshLogsButton_clicked()
{
    ui->logsTextBrowser->setText(updater->data.logs);
}
