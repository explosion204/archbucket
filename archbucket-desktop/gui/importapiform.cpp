#include "importapiform.h"
#include "ui_importapiform.h"

ImportApiForm::ImportApiForm(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ImportApiForm)
{
    ui->setupUi(this);
}

ImportApiForm::~ImportApiForm()
{
    delete ui;
}
