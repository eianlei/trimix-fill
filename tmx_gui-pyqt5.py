#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# tmx_gui_pyqt5.py
# github project https://github.com/eianlei/trimix-fill/
# Python-3 GUI using trimix blending calculator
#  uses PyQt5 framework
#  this GUI uses function tmx_calc
# use at your own risk, no guarantees, no liability!
#
# TODO add the ppo2 input SB
# TODO print also the date/time + cost + MOD
# TODO add HELP, EXIT
# TODO add error popup dialog
# TODO add a combobox for standard mixes
# TODO fix the 300 bar bug
# TODO change the start_pressSB max according to tankEndPressComboBox

tmx_gui_version = "0.1"

# import modules, like PyQt5 stuff
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
                             QLabel, QWidget, QPushButton, QSpinBox, QDoubleSpinBox,
                             QRadioButton, QTextEdit)

# import calculation modules
from tmx_calc import *


# define the main window GUI objects and callbacks
class tmx_gui_win(QWidget):
    '''GUI for calculating trimix fills using PyQt5'''
    def __init__(self):
        super(tmx_gui_win, self).__init__()

        # GroupBox to hold starting tank mix spinboxes and labels for them
        startGroup = QGroupBox("Current tank mix")
        # define SpinBoxes to input data
        # input for current/starting pressure
        start_pressLabel = QLabel("Current tank pressure (bar):")
        self.start_pressSB = QSpinBox()
        self.start_pressSB.setRange(0, 300)  # min 0, max 300 bar
        self.start_pressSB.setSingleStep(1)  # steps of 1
        self.start_pressSB.setSuffix(' bar')  # show bar suffix
        self.start_pressSB.setValue(100)  # default is 100 bar
        self.start_pressSB.setToolTip("the starting pressure of the tank to be filled")

        # input for current/starting O2%
        start_O2pctLabel = QLabel("Current Oxygen %:")
        self.start_O2pctSB = QSpinBox()
        self.start_O2pctSB.setRange(10, 100)  # min 10%, max 100% O2
        self.start_O2pctSB.setSingleStep(1)  # steps of 1
        self.start_O2pctSB.setSuffix('%')  # show % suffix
        self.start_O2pctSB.setValue(21)  # default is air

        # input for current He%
        start_HEpctLabel = QLabel("Current Helium %:")
        self.start_HEpctSB = QSpinBox()
        self.start_HEpctSB.setRange(0, 100)  # min 0%, max 100% He
        self.start_HEpctSB.setSingleStep(1)  # steps of 1
        self.start_HEpctSB.setSuffix('%')  # show % suffix
        self.start_HEpctSB.setValue(35)  # default is 35 for tmx21/35

        # layout the group into grid
        startLayout = QGridLayout()
        startLayout.addWidget(start_pressLabel, 0, 0)
        startLayout.addWidget(self.start_pressSB, 0, 1)
        startLayout.addWidget(start_O2pctLabel, 1, 0)
        startLayout.addWidget(self.start_O2pctSB, 1, 1)
        startLayout.addWidget(start_HEpctLabel, 2, 0)
        startLayout.addWidget(self.start_HEpctSB, 2, 1)
        startGroup.setLayout(startLayout)

        # GroupBox to hold WANTED tank mix spinboxes and labels for them
        wantGroup = QGroupBox("Wanted tank mix")
        # define SpinBoxes to input data
        # input for wanted pressure, a combobox
        want_pressLabel = QLabel("Wanted tank pressure (bar):")
        self.want_pressSB = QSpinBox()
        self.tankEndPressComboBox = QComboBox()
        self.tankTypeList = ['200', '232', '300']
        for i in range(len(self.tankTypeList)) :
            self.tankEndPressComboBox.addItem(self.tankTypeList[i])

        # input for wanted O2%
        want_O2pctLabel = QLabel("Wanted Oxygen %:")
        self.want_O2pctSB = QSpinBox()
        self.want_O2pctSB.setRange(10, 100)  # min 10%, max 100% O2
        self.want_O2pctSB.setSingleStep(1)  # steps of 1
        self.want_O2pctSB.setSuffix('%')  # show % suffix
        self.want_O2pctSB.setValue(21)  # default is air

        # input for wanted He%
        want_HEpctLabel = QLabel("Wanted Helium %:")
        self.want_HEpctSB = QSpinBox()
        self.want_HEpctSB.setRange(0, 100)  # min 0%, max 100% He
        self.want_HEpctSB.setSingleStep(1)  # steps of 1
        self.want_HEpctSB.setSuffix('%')  # show % suffix
        self.want_HEpctSB.setValue(35)  # default is 35 for tmx21/35

        # layout the group into grid
        wantLayout = QGridLayout()
        wantLayout.addWidget(want_pressLabel, 0, 0)
        wantLayout.addWidget(self.tankEndPressComboBox, 0, 1)
        wantLayout.addWidget(want_O2pctLabel, 1, 0)
        wantLayout.addWidget(self.want_O2pctSB, 1, 1)
        wantLayout.addWidget(want_HEpctLabel, 2, 0)
        wantLayout.addWidget(self.want_HEpctSB, 2, 1)
        wantGroup.setLayout(wantLayout)

        # GroupBox to hold fill cost calculation spinboxes and labels for them
        costGroup = QGroupBox("Fill cost calculation input")
        # define SpinBoxes to input data
        # input for tank size
        tankSizeLabel = QLabel("Tank size (liters):")
        self.tankSizeSB = QSpinBox()
        self.tankSizeSB.setRange(1, 50)  # min 1, max 50 liters
        self.tankSizeSB.setSingleStep(1)  # steps of 1
        self.tankSizeSB.setSuffix(' L')  # show L suffix
        self.tankSizeSB.setValue(24)  # default is 24 liters
        # input Oxygen cost
        o2costLabel = QLabel("Oxygen cost (€/m^3):")
        self.o2costSB = QDoubleSpinBox()
        self.o2costSB.setRange(1.0, 50.0)  # min - max
        self.o2costSB.setSingleStep(0.1)  # steps of 0.1
        self.o2costSB.setSuffix(' €/m^3')  # show suffix
        self.o2costSB.setValue(4.14)  # default
        # input Helium cost
        HEcostLabel = QLabel("Helium cost (€/m^3):")
        self.HEcostSB = QDoubleSpinBox()
        self.HEcostSB.setRange(1.0, 500.0)  # min - max
        self.HEcostSB.setSingleStep(0.1)  # steps of 0.1
        self.HEcostSB.setSuffix(' €/m^3')  # show suffix
        self.HEcostSB.setValue(25.0)  # default
        # input compress fill cost
        compCostLabel = QLabel("compressor run cost (€):")
        self.compCostSB = QDoubleSpinBox()
        self.compCostSB.setRange(1.0, 50.0)  # min - max
        self.compCostSB.setSingleStep(0.01)  # steps of 0.1
        self.compCostSB.setSuffix(' €')  # show suffix
        self.compCostSB.setValue(5.00)  # default

        costLayout = QGridLayout()
        costLayout.addWidget(tankSizeLabel, 0, 0)
        costLayout.addWidget(self.tankSizeSB, 0, 1)
        costLayout.addWidget(o2costLabel, 1, 0)
        costLayout.addWidget(self.o2costSB, 1, 1)
        costLayout.addWidget(HEcostLabel, 2, 0)
        costLayout.addWidget(self.HEcostSB, 2, 1)
        costLayout.addWidget(compCostLabel, 3, 0)
        costLayout.addWidget(self.compCostSB, 3, 1)
        costGroup.setLayout(costLayout)

        # radiobuttons to select fill methods
        self.fill_method = "tmx"
        fmGroup   = QGroupBox("Select fill method")
        fmLayout  = QGridLayout()
        fillRBpp  = QRadioButton("Partial pressure fill (O2+He+air)")
        fillRBpp.clicked.connect(self.rb_pp)
        fillRBcfm = QRadioButton("Helium + CFM")
        fillRBcfm.clicked.connect(self.rb_cfm)
        fillRBtmx = QRadioButton("Trimix CFM")
        fillRBtmx.setChecked(True)
        fillRBtmx.clicked.connect(self.rb_tmx)
        fillRBair = QRadioButton("air fill")
        fillRBair.clicked.connect(self.rb_air)
        fillRBnx  = QRadioButton("Nitrox CFM")
        fillRBnx.clicked.connect(self.rb_nx)
        fmLayout.addWidget(fillRBpp, 0, 0)
        fmLayout.addWidget(fillRBcfm, 1, 0)
        fmLayout.addWidget(fillRBtmx, 2, 0)
        fmLayout.addWidget(fillRBair, 0, 1)
        fmLayout.addWidget(fillRBnx, 1, 1)
        fmGroup.setLayout(fmLayout)

        # lay out buttons
        btnGroup = QGroupBox("PRESS BUTTONS FOR ACTIONS")
        btnLayout = QGridLayout()
        self.CalculateBtn = QPushButton('CALCULATE', self)
        self.CalculateBtn.clicked.connect(self.calc_button_clicked)
        btnLayout.addWidget(self.CalculateBtn, 0,0)
        btnGroup.setLayout(btnLayout)

        # QText for output
        self.outTxt = QTextEdit()

        ################################################
        # lay out all sub grids to top level grid
        layout = QGridLayout()
        layout.addWidget(startGroup, 0, 0)
        layout.addWidget(wantGroup, 1, 0)
        layout.addWidget(costGroup, 0, 1)
        layout.addWidget(fmGroup,2,0,1,2)
        layout.addWidget(btnGroup,1,1)
        layout.addWidget(self.outTxt,3,0,4,2)
        self.setLayout(layout)

        # window title, and we are done
        self.setWindowTitle("Trimix blending calculator PyQt5 v {}".format(tmx_gui_version))
        self.outTxt.setPlainText("tmx_gui-pyqt5.py ready")
        self.outTxt.append("Enter input and click CALCULATE\n")

    def rb_pp(self):
        self.fill_method = "pp"
        pass
    def rb_cfm(self):
        self.fill_method = "cfm"
        pass
    def rb_tmx(self):
        self.fill_method = "tmx"
        pass
    def rb_air(self):
        self.fill_method = "air"
        pass
    def rb_nx(self):
        self.fill_method = "nx"
        pass

    def calc_button_clicked(self):
        calc_method = self.fill_method

        print("tmx_gui: calculate")
        # get data from GUI objects, then convert input strings to floats
        startbar = self.start_pressSB.value()
        endbar = float(self.tankEndPressComboBox.currentText())
        start_o2 =  self.start_O2pctSB.value()
        start_he =  self.start_HEpctSB.value()
        end_o2 =  self.want_O2pctSB.value()
        end_he =  self.want_HEpctSB.value()
        ppo2in =  1.6
        # cost calculation input
        liters =  self.tankSizeSB.value()
        o2_cost_eur =  self.o2costSB.value()
        he_cost_eur =  self.HEcostSB.value()
        fill_cost_eur =  self.compCostSB.value()
        he_ig = False
        o2_ig = False

        print("calculate with: ")
        print(calc_method, startbar, endbar, start_o2, start_he,
              end_o2, end_he, ppo2in, he_ig, o2_ig)
        #
        result = tmx_calc(calc_method, startbar, endbar, start_o2, start_he,
                          end_o2, end_he, he_ig, o2_ig)
        self.outTxt.append(result['status_text'])
        self.outTxt.moveCursor(QtGui.QTextCursor.End)

        pass

# main window loop starts now
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = tmx_gui_win()
    window.show()
    sys.exit(app.exec_())
# done, end of application
