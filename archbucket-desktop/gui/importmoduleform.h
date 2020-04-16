#ifndef IMPORTMODULEFORM_H
#define IMPORTMODULEFORM_H

#include <QWidget>

namespace Ui {
class ImportModuleForm;
}

class ImportModuleForm : public QWidget
{
    Q_OBJECT

public:
    explicit ImportModuleForm(QWidget *parent = nullptr);
    ~ImportModuleForm();

private:
    Ui::ImportModuleForm *ui;
};

#endif // IMPORTMODULEFORM_H
