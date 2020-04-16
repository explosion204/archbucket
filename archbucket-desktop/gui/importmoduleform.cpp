#include "importmoduleform.h"
#include "ui_importmoduleform.h"

ImportModuleForm::ImportModuleForm(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ImportModuleForm)
{
    ui->setupUi(this);
}

ImportModuleForm::~ImportModuleForm()
{
    delete ui;
}
