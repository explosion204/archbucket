#ifndef IMPORTAPIFORM_H
#define IMPORTAPIFORM_H

#include <QWidget>
#include <QFileDialog>
#include <QMessageBox>

#include "net/updater.h"

namespace Ui {
class ImportApiForm;
}

class ImportApiForm : public QWidget
{
    Q_OBJECT

public:
    explicit ImportApiForm(Updater *updater, QWidget *parent = nullptr);
    ~ImportApiForm();

private slots:
    void on_openButton_clicked();

    void on_importButton_clicked();

private:
    Ui::ImportApiForm *ui;
    QWidget *parent;
    Updater *updater;
    QFile *file;
};

#endif // IMPORTAPIFORM_H
