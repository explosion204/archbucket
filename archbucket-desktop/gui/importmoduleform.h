#ifndef IMPORTMODULEFORM_H
#define IMPORTMODULEFORM_H

#include <QDialog>
#include <QFileDialog>
#include <QMessageBox>
#include <QMovie>

#include "net/updater.h"

namespace Ui {
class ImportModuleForm;
}

class ImportModuleForm : public QDialog
{
    Q_OBJECT

public:
    explicit ImportModuleForm(Updater *updater, QWidget *parent = nullptr);
    ~ImportModuleForm();

signals:
    void importing_ended(bool result, QString message);

private slots:
    void on_openButton_clicked();
    void on_importButton_clicked();
    void on_importing_ended(bool result, QString message);

private:
    Ui::ImportModuleForm *ui;
    Updater *updater;
    QWidget *parent;
    QFile *file;
    QMovie *loading_movie;

    void setButtonIcon();
};

#endif // IMPORTMODULEFORM_H
