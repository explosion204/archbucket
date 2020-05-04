#include "importapiform.h"
#include "ui_importapiform.h"

ImportApiForm::ImportApiForm(Updater *updater, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ImportApiForm)
{
    ui->setupUi(this);
    this->updater = updater;
    this->parent = parent;
    loading_movie = new QMovie(":/gifs/assets/loading.gif");
}

ImportApiForm::~ImportApiForm()
{
    delete ui;

    if (file->isOpen())
        file->close();

    delete file;
    delete loading_movie;
}

void ImportApiForm::on_openButton_clicked()
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


void ImportApiForm::on_importButton_clicked()
{
    if (!ui->nameEdit->text().isEmpty() && !ui->classNameEdit->text().isEmpty())
    {
        QByteArray source_code = file->readAll();
        file->close();

        loading_movie->start();
        ui->importButton->setEnabled(false);

        connect(this, &ImportApiForm::importing_ended, this, &ImportApiForm::on_importing_ended);

        std::thread([this, source_code] ()
        {
            auto response = updater->importApiModule(ui->nameEdit->text(), ui->classNameEdit->text(), QString::fromLocal8Bit(source_code));
            importing_ended(response.first, response.second);
            loading_movie->stop();
        }).detach();
    }
}

void ImportApiForm::setButtonIcon()
{
    ui->importButton->setIcon(QIcon(loading_movie->currentPixmap()));
}

void ImportApiForm::on_importing_ended(bool result, QString message)
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
