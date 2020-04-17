#ifndef MAINFORM_H
#define MAINFORM_H

#include <QWidget>
#include <QMessageBox>
#include <QListWidgetItem>

#include "net/updater.h"
#include "gui/loginform.h"
#include "gui/importapiform.h"
#include "gui/importmoduleform.h"

namespace Ui {
class MainForm;
}

class MainForm : public QWidget
{
    Q_OBJECT

public:
    explicit MainForm(Updater *updater, QWidget *parent = nullptr);
    ~MainForm();

private slots:
    void on_connection_broken();
    void updateStatus();
    void updateListWidgets();

    void on_startBotButton_clicked();
    void on_apiList_itemChanged(QListWidgetItem *item);
    void on_modulesList_itemChanged(QListWidgetItem *item);
    void on_refreshApiListButton_clicked();
    void on_refreshModuleList_clicked();

    void on_stopBotButton_clicked();

    void on_restartBptButton_clicked();

    void on_importApiButton_clicked();

    void on_importModuleButton_clicked();

private:
    Ui::MainForm *ui;
    Updater *updater;
};

#endif // MAINFORM_H
