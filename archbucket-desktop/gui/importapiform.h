#ifndef IMPORTAPIFORM_H
#define IMPORTAPIFORM_H

#include <QWidget>

namespace Ui {
class ImportApiForm;
}

class ImportApiForm : public QWidget
{
    Q_OBJECT

public:
    explicit ImportApiForm(QWidget *parent = nullptr);
    ~ImportApiForm();

private:
    Ui::ImportApiForm *ui;
};

#endif // IMPORTAPIFORM_H
