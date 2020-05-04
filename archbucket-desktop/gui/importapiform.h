#ifndef IMPORTAPIFORM_H
#define IMPORTAPIFORM_H

#include <QDialog>
#include <QFileDialog>
#include <QMessageBox>
#include <QMovie>

#include "net/updater.h"

namespace Ui {
class ImportApiForm;
}

class ImportApiForm : public QDialog
{
    Q_OBJECT

public:
    explicit ImportApiForm(Updater *updater, QWidget *parent = nullptr);
    ~ImportApiForm();

signals:
    void importing_ended(bool result, QString message);

private slots:
    void on_openButton_clicked();
    void on_importButton_clicked();
    void on_importing_ended(bool result, QString message);

private:
    Ui::ImportApiForm *ui;
    QWidget *parent;
    Updater *updater;
    QFile *file;
    QMovie *loading_movie;

    void setButtonIcon();
};

#endif // IMPORTAPIFORM_H
