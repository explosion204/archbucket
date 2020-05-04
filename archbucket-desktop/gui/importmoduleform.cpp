#include "importmoduleform.h"
#include "ui_importmoduleform.h"

ImportModuleForm::ImportModuleForm(Updater *updater, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ImportModuleForm)
{
    ui->setupUi(this);
    this->updater = updater;
    this->parent = parent;
    loading_movie = new QMovie(":/gifs/assets/loading.gif");

    connect(loading_movie, &QMovie::frameChanged, this, &ImportModuleForm::setButtonIcon);
    if (loading_movie->loopCount() != -1)
        connect(loading_movie, &QMovie::finished, loading_movie, &QMovie::start);

}

ImportModuleForm::~ImportModuleForm()
{
    delete ui;

    if (file->isOpen())
        file->close();

    delete file;
    delete loading_movie;
}

void ImportModuleForm::on_openButton_clicked()
{
    QString file_path = QFileDialog::getOpenFileName(this, tr("Open file with Python source code"), "");

    if (!file_path.isEmpty())
    {
        ui->pathEdit->setText(file_path);
        file = new QFile(file_path);
        file->open(QIODevice::Text);

        ui->importButton->setEnabled(true);
    }
}

void ImportModuleForm::on_importButton_clicked()
{
    if (!ui->nameEdit->text().isEmpty())
    {
        QByteArray source_code = file->readAll();
        file->close();

        loading_movie->start();
        ui->importButton->setEnabled(false);

        connect(this, &ImportModuleForm::importing_ended, this, &ImportModuleForm::on_importing_ended);

        std::thread([this, source_code] ()
        {
            auto response = updater->importModule(ui->nameEdit->text(), QString::fromLocal8Bit(source_code));
            importing_ended(response.first, response.second);
            loading_movie->stop();
        }).detach();
    }
}

void ImportModuleForm::setButtonIcon()
{
    ui->importButton->setIcon(QIcon(loading_movie->currentPixmap()));
}

void ImportModuleForm::on_importing_ended(bool result, QString message)
{
    if (result)
    {
        QMessageBox::information(parent, "Info", message);
    }
    else
    {
        QMessageBox::warning(parent, "Error", message);
    }

    close();
}
