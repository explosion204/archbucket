#include "importapiform.h"
#include "ui_importapiform.h"

ImportApiForm::ImportApiForm(Updater *updater, QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ImportApiForm)
{
    ui->setupUi(this);
    this->updater = updater;
    this->parent = parent;
}

ImportApiForm::~ImportApiForm()
{
    delete ui;

    if (file->isOpen())
        file->close();

    delete file;
}

void ImportApiForm::on_openButton_clicked()
{
    QString file_path = QFileDialog::getOpenFileName(this, tr("Open file with Python source code"), "");
    ui->pathEdit->setText(file_path);

    file = new QFile(file_path);
    file->open(QIODevice::Text);

    ui->importButton->setEnabled(true);
}


void ImportApiForm::on_importButton_clicked()
{
    if (!ui->nameEdit->text().isEmpty() && !ui->classNameEdit->text().isEmpty())
    {
        QByteArray source_code = file->readAll();
        file->close();

        auto response = updater->importApiModule(ui->nameEdit->text(), ui->classNameEdit->text(), QString::fromLocal8Bit(source_code));
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
