# Form implementation generated from reading ui file '.\销售管理主界面.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(920, 559)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.DIYSearchCheckBox = QtWidgets.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DIYSearchCheckBox.setFont(font)
        self.DIYSearchCheckBox.setObjectName("DIYSearchCheckBox")
        self.horizontalLayout_6.addWidget(self.DIYSearchCheckBox)
        self.ResetButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ResetButton.setFont(font)
        self.ResetButton.setObjectName("ResetButton")
        self.horizontalLayout_6.addWidget(self.ResetButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.StartDateVerLay = QtWidgets.QVBoxLayout()
        self.StartDateVerLay.setObjectName("StartDateVerLay")
        self.StartDateLabel = QtWidgets.QLabel(Form)
        self.StartDateLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.StartDateLabel.setObjectName("StartDateLabel")
        self.StartDateVerLay.addWidget(self.StartDateLabel)
        self.StartDateEdit = QtWidgets.QDateEdit(Form)
        self.StartDateEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StartDateEdit.sizePolicy().hasHeightForWidth())
        self.StartDateEdit.setSizePolicy(sizePolicy)
        self.StartDateEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.StartDateEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.StartDateEdit.setObjectName("StartDateEdit")
        self.StartDateVerLay.addWidget(self.StartDateEdit)
        self.horizontalLayout_10.addLayout(self.StartDateVerLay)
        self.EndDateVerLay = QtWidgets.QVBoxLayout()
        self.EndDateVerLay.setObjectName("EndDateVerLay")
        self.EndDateLabel = QtWidgets.QLabel(Form)
        self.EndDateLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EndDateLabel.setObjectName("EndDateLabel")
        self.EndDateVerLay.addWidget(self.EndDateLabel)
        self.EndDateEdit = QtWidgets.QDateEdit(Form)
        self.EndDateEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EndDateEdit.sizePolicy().hasHeightForWidth())
        self.EndDateEdit.setSizePolicy(sizePolicy)
        self.EndDateEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.EndDateEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.EndDateEdit.setMaximumDate(QtCore.QDate(9999, 12, 31))
        self.EndDateEdit.setObjectName("EndDateEdit")
        self.EndDateVerLay.addWidget(self.EndDateEdit)
        self.horizontalLayout_10.addLayout(self.EndDateVerLay)
        self.ClientVerLay = QtWidgets.QVBoxLayout()
        self.ClientVerLay.setObjectName("ClientVerLay")
        self.ClientLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ClientLabel.sizePolicy().hasHeightForWidth())
        self.ClientLabel.setSizePolicy(sizePolicy)
        self.ClientLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ClientLabel.setObjectName("ClientLabel")
        self.ClientVerLay.addWidget(self.ClientLabel)
        self.ClientComBox = QtWidgets.QComboBox(Form)
        self.ClientComBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ClientComBox.sizePolicy().hasHeightForWidth())
        self.ClientComBox.setSizePolicy(sizePolicy)
        self.ClientComBox.setMinimumSize(QtCore.QSize(125, 25))
        self.ClientComBox.setMaximumSize(QtCore.QSize(16777215, 25))
        self.ClientComBox.setEditable(True)
        self.ClientComBox.setObjectName("ClientComBox")
        self.ClientComBox.addItem("")
        self.ClientVerLay.addWidget(self.ClientComBox)
        self.horizontalLayout_10.addLayout(self.ClientVerLay)
        self.PaymVerLay = QtWidgets.QVBoxLayout()
        self.PaymVerLay.setObjectName("PaymVerLay")
        self.PaymLabel = QtWidgets.QLabel(Form)
        self.PaymLabel.setObjectName("PaymLabel")
        self.PaymVerLay.addWidget(self.PaymLabel)
        self.PaymComBox = QtWidgets.QComboBox(Form)
        self.PaymComBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PaymComBox.sizePolicy().hasHeightForWidth())
        self.PaymComBox.setSizePolicy(sizePolicy)
        self.PaymComBox.setMinimumSize(QtCore.QSize(0, 25))
        self.PaymComBox.setMaximumSize(QtCore.QSize(16777215, 25))
        self.PaymComBox.setEditable(False)
        self.PaymComBox.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)
        self.PaymComBox.setObjectName("PaymComBox")
        self.PaymComBox.addItem("")
        self.PaymComBox.addItem("")
        self.PaymComBox.addItem("")
        self.PaymComBox.addItem("")
        self.PaymVerLay.addWidget(self.PaymComBox)
        self.horizontalLayout_10.addLayout(self.PaymVerLay)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.UpperLimitCheckBox = QtWidgets.QCheckBox(Form)
        self.UpperLimitCheckBox.setEnabled(False)
        self.UpperLimitCheckBox.setObjectName("UpperLimitCheckBox")
        self.horizontalLayout_3.addWidget(self.UpperLimitCheckBox)
        self.UpperLimitLineEdit = QtWidgets.QLineEdit(Form)
        self.UpperLimitLineEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UpperLimitLineEdit.sizePolicy().hasHeightForWidth())
        self.UpperLimitLineEdit.setSizePolicy(sizePolicy)
        self.UpperLimitLineEdit.setMinimumSize(QtCore.QSize(50, 25))
        self.UpperLimitLineEdit.setMaximumSize(QtCore.QSize(75, 25))
        self.UpperLimitLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.UpperLimitLineEdit.setObjectName("UpperLimitLineEdit")
        self.horizontalLayout_3.addWidget(self.UpperLimitLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LowerLimitCheckBox = QtWidgets.QCheckBox(Form)
        self.LowerLimitCheckBox.setEnabled(False)
        self.LowerLimitCheckBox.setObjectName("LowerLimitCheckBox")
        self.horizontalLayout.addWidget(self.LowerLimitCheckBox)
        self.LowerLimitLineEdit = QtWidgets.QLineEdit(Form)
        self.LowerLimitLineEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LowerLimitLineEdit.sizePolicy().hasHeightForWidth())
        self.LowerLimitLineEdit.setSizePolicy(sizePolicy)
        self.LowerLimitLineEdit.setMinimumSize(QtCore.QSize(50, 25))
        self.LowerLimitLineEdit.setMaximumSize(QtCore.QSize(75, 25))
        self.LowerLimitLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LowerLimitLineEdit.setObjectName("LowerLimitLineEdit")
        self.horizontalLayout.addWidget(self.LowerLimitLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.debt = QtWidgets.QHBoxLayout()
        self.debt.setObjectName("debt")
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.debt.addWidget(self.label_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.DebtUpperLimitCheckBox = QtWidgets.QCheckBox(Form)
        self.DebtUpperLimitCheckBox.setEnabled(False)
        self.DebtUpperLimitCheckBox.setObjectName("DebtUpperLimitCheckBox")
        self.horizontalLayout_8.addWidget(self.DebtUpperLimitCheckBox)
        self.DebtUpperLimitLineEdit = QtWidgets.QLineEdit(Form)
        self.DebtUpperLimitLineEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DebtUpperLimitLineEdit.sizePolicy().hasHeightForWidth())
        self.DebtUpperLimitLineEdit.setSizePolicy(sizePolicy)
        self.DebtUpperLimitLineEdit.setMinimumSize(QtCore.QSize(50, 25))
        self.DebtUpperLimitLineEdit.setMaximumSize(QtCore.QSize(75, 25))
        self.DebtUpperLimitLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.DebtUpperLimitLineEdit.setObjectName("DebtUpperLimitLineEdit")
        self.horizontalLayout_8.addWidget(self.DebtUpperLimitLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.DebtLowerLimitCheckBox = QtWidgets.QCheckBox(Form)
        self.DebtLowerLimitCheckBox.setEnabled(False)
        self.DebtLowerLimitCheckBox.setObjectName("DebtLowerLimitCheckBox")
        self.horizontalLayout_9.addWidget(self.DebtLowerLimitCheckBox)
        self.DebtLowerLimitLineEdit = QtWidgets.QLineEdit(Form)
        self.DebtLowerLimitLineEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DebtLowerLimitLineEdit.sizePolicy().hasHeightForWidth())
        self.DebtLowerLimitLineEdit.setSizePolicy(sizePolicy)
        self.DebtLowerLimitLineEdit.setMinimumSize(QtCore.QSize(50, 25))
        self.DebtLowerLimitLineEdit.setMaximumSize(QtCore.QSize(75, 25))
        self.DebtLowerLimitLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.DebtLowerLimitLineEdit.setObjectName("DebtLowerLimitLineEdit")
        self.horizontalLayout_9.addWidget(self.DebtLowerLimitLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.debt.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addLayout(self.debt)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.DeleteButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeleteButton.sizePolicy().hasHeightForWidth())
        self.DeleteButton.setSizePolicy(sizePolicy)
        self.DeleteButton.setMinimumSize(QtCore.QSize(50, 30))
        self.DeleteButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.DeleteButton.setFont(font)
        self.DeleteButton.setObjectName("DeleteButton")
        self.verticalLayout_6.addWidget(self.DeleteButton)
        self.SearchButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchButton.sizePolicy().hasHeightForWidth())
        self.SearchButton.setSizePolicy(sizePolicy)
        self.SearchButton.setMinimumSize(QtCore.QSize(50, 30))
        self.SearchButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.SearchButton.setFont(font)
        self.SearchButton.setObjectName("SearchButton")
        self.verticalLayout_6.addWidget(self.SearchButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.CreateNewOrderButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CreateNewOrderButton.sizePolicy().hasHeightForWidth())
        self.CreateNewOrderButton.setSizePolicy(sizePolicy)
        self.CreateNewOrderButton.setMinimumSize(QtCore.QSize(50, 30))
        self.CreateNewOrderButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CreateNewOrderButton.setFont(font)
        self.CreateNewOrderButton.setObjectName("CreateNewOrderButton")
        self.horizontalLayout_2.addWidget(self.CreateNewOrderButton)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        self.tree = QtWidgets.QTreeWidget(Form)
        self.tree.setMinimumSize(QtCore.QSize(0, 300))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tree.setFont(font)
        self.tree.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AnyKeyPressed|QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked|QtWidgets.QAbstractItemView.EditTrigger.SelectedClicked)
        self.tree.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.NoDragDrop)
        self.tree.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.setUniformRowHeights(True)
        self.tree.setObjectName("tree")
        self.tree.headerItem().setTextAlignment(0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(2, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(3, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(4, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(5, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(6, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(7, QtCore.Qt.AlignmentFlag.AlignCenter)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree)
        self.tree.header().setCascadingSectionResizes(True)
        self.tree.header().setDefaultSectionSize(110)
        self.tree.header().setHighlightSections(True)
        self.tree.header().setSortIndicatorShown(False)
        self.tree.header().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.tree)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.Selected = QtWidgets.QHBoxLayout()
        self.Selected.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.Selected.setObjectName("Selected")
        self.SelectedBoxes = QtWidgets.QHBoxLayout()
        self.SelectedBoxes.setObjectName("SelectedBoxes")
        self.SelectedBoxesTextLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedBoxesTextLabel.sizePolicy().hasHeightForWidth())
        self.SelectedBoxesTextLabel.setSizePolicy(sizePolicy)
        self.SelectedBoxesTextLabel.setMinimumSize(QtCore.QSize(40, 15))
        self.SelectedBoxesTextLabel.setMaximumSize(QtCore.QSize(75, 15))
        self.SelectedBoxesTextLabel.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.SelectedBoxesTextLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.SelectedBoxesTextLabel.setObjectName("SelectedBoxesTextLabel")
        self.SelectedBoxes.addWidget(self.SelectedBoxesTextLabel)
        self.SelectedBoxesNumLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedBoxesNumLabel.sizePolicy().hasHeightForWidth())
        self.SelectedBoxesNumLabel.setSizePolicy(sizePolicy)
        self.SelectedBoxesNumLabel.setMaximumSize(QtCore.QSize(150, 15))
        self.SelectedBoxesNumLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.SelectedBoxesNumLabel.setWordWrap(False)
        self.SelectedBoxesNumLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.SelectedBoxesNumLabel.setObjectName("SelectedBoxesNumLabel")
        self.SelectedBoxes.addWidget(self.SelectedBoxesNumLabel)
        self.Selected.addLayout(self.SelectedBoxes)
        self.SelectedPcs = QtWidgets.QHBoxLayout()
        self.SelectedPcs.setObjectName("SelectedPcs")
        self.SelectedPcsTextLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedPcsTextLabel.sizePolicy().hasHeightForWidth())
        self.SelectedPcsTextLabel.setSizePolicy(sizePolicy)
        self.SelectedPcsTextLabel.setMinimumSize(QtCore.QSize(40, 15))
        self.SelectedPcsTextLabel.setMaximumSize(QtCore.QSize(75, 15))
        self.SelectedPcsTextLabel.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.SelectedPcsTextLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.SelectedPcsTextLabel.setObjectName("SelectedPcsTextLabel")
        self.SelectedPcs.addWidget(self.SelectedPcsTextLabel)
        self.SelectedPcsNumLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedPcsNumLabel.sizePolicy().hasHeightForWidth())
        self.SelectedPcsNumLabel.setSizePolicy(sizePolicy)
        self.SelectedPcsNumLabel.setMaximumSize(QtCore.QSize(150, 15))
        self.SelectedPcsNumLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.SelectedPcsNumLabel.setWordWrap(False)
        self.SelectedPcsNumLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.SelectedPcsNumLabel.setObjectName("SelectedPcsNumLabel")
        self.SelectedPcs.addWidget(self.SelectedPcsNumLabel)
        self.Selected.addLayout(self.SelectedPcs)
        self.SelectedAmount = QtWidgets.QHBoxLayout()
        self.SelectedAmount.setObjectName("SelectedAmount")
        self.SelectedAmountTextLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedAmountTextLabel.sizePolicy().hasHeightForWidth())
        self.SelectedAmountTextLabel.setSizePolicy(sizePolicy)
        self.SelectedAmountTextLabel.setMinimumSize(QtCore.QSize(40, 15))
        self.SelectedAmountTextLabel.setMaximumSize(QtCore.QSize(75, 15))
        self.SelectedAmountTextLabel.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.SelectedAmountTextLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.SelectedAmountTextLabel.setObjectName("SelectedAmountTextLabel")
        self.SelectedAmount.addWidget(self.SelectedAmountTextLabel)
        self.SelectedAmountNumLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedAmountNumLabel.sizePolicy().hasHeightForWidth())
        self.SelectedAmountNumLabel.setSizePolicy(sizePolicy)
        self.SelectedAmountNumLabel.setMaximumSize(QtCore.QSize(150, 15))
        self.SelectedAmountNumLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.SelectedAmountNumLabel.setWordWrap(False)
        self.SelectedAmountNumLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.SelectedAmountNumLabel.setObjectName("SelectedAmountNumLabel")
        self.SelectedAmount.addWidget(self.SelectedAmountNumLabel)
        self.Selected.addLayout(self.SelectedAmount)
        self.horizontalLayout_7.addLayout(self.Selected)
        self.blank = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blank.sizePolicy().hasHeightForWidth())
        self.blank.setSizePolicy(sizePolicy)
        self.blank.setText("")
        self.blank.setObjectName("blank")
        self.horizontalLayout_7.addWidget(self.blank)
        self.TotAmount = QtWidgets.QHBoxLayout()
        self.TotAmount.setObjectName("TotAmount")
        self.TotAmountTextLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TotAmountTextLabel.sizePolicy().hasHeightForWidth())
        self.TotAmountTextLabel.setSizePolicy(sizePolicy)
        self.TotAmountTextLabel.setMinimumSize(QtCore.QSize(40, 15))
        self.TotAmountTextLabel.setMaximumSize(QtCore.QSize(51, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.TotAmountTextLabel.setFont(font)
        self.TotAmountTextLabel.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.TotAmountTextLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.TotAmountTextLabel.setObjectName("TotAmountTextLabel")
        self.TotAmount.addWidget(self.TotAmountTextLabel)
        self.TotAmountNumLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TotAmountNumLabel.sizePolicy().hasHeightForWidth())
        self.TotAmountNumLabel.setSizePolicy(sizePolicy)
        self.TotAmountNumLabel.setMaximumSize(QtCore.QSize(150, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.TotAmountNumLabel.setFont(font)
        self.TotAmountNumLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.TotAmountNumLabel.setWordWrap(False)
        self.TotAmountNumLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.TotAmountNumLabel.setObjectName("TotAmountNumLabel")
        self.TotAmount.addWidget(self.TotAmountNumLabel)
        self.horizontalLayout_7.addLayout(self.TotAmount)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.DIYSearchCheckBox.clicked['bool'].connect(self.StartDateEdit.setEnabled) # type: ignore
        self.DIYSearchCheckBox.clicked['bool'].connect(self.EndDateEdit.setEnabled) # type: ignore
        self.DIYSearchCheckBox.clicked['bool'].connect(self.ClientComBox.setEnabled) # type: ignore
        self.DIYSearchCheckBox.clicked['bool'].connect(self.PaymComBox.setEnabled) # type: ignore
        self.DIYSearchCheckBox.clicked['bool'].connect(self.LowerLimitCheckBox.setEnabled) # type: ignore
        self.DIYSearchCheckBox.clicked['bool'].connect(self.UpperLimitCheckBox.setEnabled) # type: ignore
        self.LowerLimitCheckBox.clicked['bool'].connect(self.LowerLimitLineEdit.setEnabled) # type: ignore
        self.UpperLimitCheckBox.clicked['bool'].connect(self.UpperLimitLineEdit.setEnabled) # type: ignore
        self.DIYSearchCheckBox.clicked['bool'].connect(self.DebtUpperLimitCheckBox.setEnabled) # type: ignore
        self.DIYSearchCheckBox.clicked['bool'].connect(self.DebtLowerLimitCheckBox.setEnabled) # type: ignore
        self.DebtUpperLimitCheckBox.clicked['bool'].connect(self.DebtUpperLimitLineEdit.setEnabled) # type: ignore
        self.DebtLowerLimitCheckBox.clicked['bool'].connect(self.DebtLowerLimitLineEdit.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.DIYSearchCheckBox.setText(_translate("Form", "开启自定义查询？"))
        self.ResetButton.setText(_translate("Form", "重置"))
        self.StartDateLabel.setText(_translate("Form", "开始日期"))
        self.StartDateEdit.setDisplayFormat(_translate("Form", "yyyy/MM/dd"))
        self.EndDateLabel.setText(_translate("Form", "结束日期"))
        self.EndDateEdit.setDisplayFormat(_translate("Form", "yyyy/MM/dd"))
        self.ClientLabel.setText(_translate("Form", "客户"))
        self.ClientComBox.setItemText(0, _translate("Form", "--"))
        self.PaymLabel.setText(_translate("Form", "付款方式"))
        self.PaymComBox.setItemText(0, _translate("Form", "--"))
        self.PaymComBox.setItemText(1, _translate("Form", "现金"))
        self.PaymComBox.setItemText(2, _translate("Form", "银行"))
        self.PaymComBox.setItemText(3, _translate("Form", "欠款"))
        self.label.setText(_translate("Form", "金额\n"
"查询"))
        self.UpperLimitCheckBox.setText(_translate("Form", "上限"))
        self.LowerLimitCheckBox.setText(_translate("Form", "下限"))
        self.label_2.setText(_translate("Form", "欠款\n"
"查询"))
        self.DebtUpperLimitCheckBox.setText(_translate("Form", "上限"))
        self.DebtLowerLimitCheckBox.setText(_translate("Form", "下限"))
        self.DeleteButton.setText(_translate("Form", "删除"))
        self.SearchButton.setText(_translate("Form", "查询"))
        self.CreateNewOrderButton.setText(_translate("Form", "新建"))
        self.tree.headerItem().setText(0, _translate("Form", "单据"))
        self.tree.headerItem().setText(1, _translate("Form", "日期"))
        self.tree.headerItem().setText(2, _translate("Form", "客户"))
        self.tree.headerItem().setText(3, _translate("Form", "箱数"))
        self.tree.headerItem().setText(4, _translate("Form", "件数"))
        self.tree.headerItem().setText(5, _translate("Form", "总金额"))
        self.tree.headerItem().setText(6, _translate("Form", "付款方式"))
        self.tree.headerItem().setText(7, _translate("Form", "欠款金额"))
        __sortingEnabled = self.tree.isSortingEnabled()
        self.tree.setSortingEnabled(False)
        self.tree.topLevelItem(0).setText(0, _translate("Form", "1"))
        self.tree.topLevelItem(0).setText(1, _translate("Form", "2022/09/23"))
        self.tree.topLevelItem(0).setText(2, _translate("Form", "Caio"))
        self.tree.topLevelItem(0).setText(3, _translate("Form", "100"))
        self.tree.topLevelItem(0).setText(4, _translate("Form", "3000"))
        self.tree.topLevelItem(0).setText(5, _translate("Form", "30000"))
        self.tree.topLevelItem(0).setText(6, _translate("Form", "银行"))
        self.tree.setSortingEnabled(__sortingEnabled)
        self.SelectedBoxesTextLabel.setText(_translate("Form", "选中箱数"))
        self.SelectedBoxesNumLabel.setText(_translate("Form", "0 箱"))
        self.SelectedPcsTextLabel.setText(_translate("Form", "选中件数"))
        self.SelectedPcsNumLabel.setText(_translate("Form", "0 件"))
        self.SelectedAmountTextLabel.setText(_translate("Form", "选中金额"))
        self.SelectedAmountNumLabel.setText(_translate("Form", "0.00 €"))
        self.TotAmountTextLabel.setText(_translate("Form", "总金额"))
        self.TotAmountNumLabel.setText(_translate("Form", "price"))
