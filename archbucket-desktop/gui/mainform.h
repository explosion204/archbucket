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

signals:
    void display_message(bool type, QString message);
    void item_removed(QListWidget *list_widget, int item_row);

private slots:
    void on_connection_broken();
    void updateStatus();
    void updateListWidgets();

    void on_startBotButton_clicked();
    void on_apiList_itemChanged(QListWidgetItem *item);
    void on_modulesList_itemChanged(QListWidgetItem *item);
    void on_refreshApiListButton_clicked();
    void on_refreshModuleListButton_clicked();
    void on_stopBotButton_clicked();
    void on_restartBotButton_clicked();
    void on_importApiButton_clicked();
    void on_importModuleButton_clicked();
    void on_removeApiButton_clicked();
    void on_removeModuleButton_clicked();

    void on_item_removed(QListWidget *list_widget, int item_row);

private:
    Ui::MainForm *ui;
    Updater *updater;
    QMovie *loading_movie;

    // loading movie will be applied to the button
    // setControlsState() do not change state of the button
    QPushButton *loading_button;

    void setLoadingButtonState(bool state);
    void on_display_message(bool type, QString message);

    void setControlsState(bool state);
};

#endif // MAINFORM_H
