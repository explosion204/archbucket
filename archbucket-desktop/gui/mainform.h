#ifndef MAINFORM_H
#define MAINFORM_H

#include <QWidget>
#include <QMessageBox>

#include "net/updater.h"
#include "gui/loginform.h"

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
    void on_connectionBroken();

private:
    Ui::MainForm *ui;
    Updater *updater;

    void updateInfo();
};

#endif // MAINFORM_H
