#include "importmoduleform.h"
#include "ui_importmoduleform.h"

ImportModuleForm::ImportModuleForm(Updater *updater, QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ImportModuleForm)
{
    ui->setupUi(this);
    this->updater = updater;
    this->parent = parent;
}

ImportModuleForm::~ImportModuleForm()
{
    delete ui;

    if (file->isOpen())
        file->close();

    delete file;
}

void ImportModuleForm::on_openButton_clicked()
{
    QString file_path = QFileDialog::getOpenFileName(this, tr("Open file with Python source code"), "");
    ui->pathEdit->setText(file_path);

    file = new QFile(file_path);
    file->open(QIODevice::Text);

    ui->importButton->setEnabled(true);
}

void ImportModuleForm::on_importButton_clicked()
{
    if (!ui->nameEdit->text().isEmpty())
    {
        QByteArray source_code = file->readAll();
        file->close();

        auto response = updater->importModule(ui->nameEdit->text(), QString::fromLocal8Bit(source_code));
        close();

        if (!response.first)
        {
            QMessageBox::warning(parent, "Error", response.second);
        }
        else
        {
            QMessageBox::information(parent, "Info", response.second);
        }

        delete this;
    }
}
