#ifndef IMPORTMODULEFORM_H
#define IMPORTMODULEFORM_H

#include <QWidget>
#include <QFileDialog>
#include <QMessageBox>
#include <QMovie>

#include "net/updater.h"

namespace Ui {
class ImportModuleForm;
}

class ImportModuleForm : public QWidget
{
    Q_OBJECT

public:
    explicit ImportModuleForm(Updater *updater, QWidget *parent = nullptr);
    ~ImportModuleForm();

private slots:
    void on_openButton_clicked();

    void on_importButton_clicked();

private:
    Ui::ImportModuleForm *ui;
    Updater *updater;
    QWidget *parent;
    QFile *file;
    QMovie *loading_movie;
};

#endif // IMPORTMODULEFORM_H
