#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# mod_gui_tk_pyqt5.py
# github project https://github.com/eianlei/trimix-fill/
#  this GUI uses function mod_calc() from tmx_calc.py
# use at your own risk, no guarantees, no liability!
#
# GUI to calculate MOD using pyqt5
#  almost same UI design as mod_gui_tk.py done with tkinter, this is with pyqt5

gui_version = "0.1"

from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
                             QLabel, QLineEdit, QWidget, QPushButton)

from tmx_calc import mod_calc


class mod_gui_win(QWidget):
    def __init__(self):
        super(mod_gui_win, self).__init__()

        modinGroup = QGroupBox("Input values for calculating MOD")

        modinmixLabel = QLabel("Std mixes:")
        modinComboBox = QComboBox()
        modinComboBox.addItem("air")
        modinComboBox.addItem("TMX 21/35")
        modinComboBox.addItem("EAN32")
        modinComboBox.addItem("EAN50")
        modinComboBox.addItem("OXYGEN")

        modin_o2pctLabel = QLabel("Oxygen %:")
        self.o2pctEdit = QLineEdit()
        # self.o2pctEdit.setValidator(QIntValidator(12,100, self.o2pctEdit))
        self.o2pctEdit.setFocus()
        modin_ppo2Label = QLabel("ppO2 in bar/ATA:")
        self.ppo2Edit = QLineEdit()
        # self.ppo2Edit.setValidator(QDoubleValidator(1.00, 2.00, 2, self.ppo2Edit))
        self.calc_btn = QPushButton('Calculate', self)
        self.calc_btn.clicked.connect(self.calc_cmd)

        modinComboBox.activated.connect(self.mix_change)

        modinLayout = QGridLayout()
        modinLayout.addWidget(modinmixLabel, 0, 0)
        modinLayout.addWidget(modinComboBox, 0, 1)
        modinLayout.addWidget(modin_o2pctLabel, 1, 0)
        modinLayout.addWidget(self.o2pctEdit, 1, 1)
        self.o2pctEdit.setText("32")
        modinLayout.addWidget(modin_ppo2Label, 2, 0)
        modinLayout.addWidget(self.ppo2Edit, 2, 1)
        self.ppo2Edit.setText("1.4")
        modinLayout.addWidget(self.calc_btn, 3, 0)

        modinGroup.setLayout(modinLayout)

        modoutGroup = QGroupBox("MOD result is")
        self.modout = QLineEdit()
        modoutLayout = QGridLayout()
        modoutLayout.addWidget(self.modout, 0, 0)
        unitLabel = QLabel("meters")
        modoutLayout.addWidget(unitLabel, 0, 1)
        modoutGroup.setLayout(modoutLayout)

        layout = QGridLayout()
        layout.addWidget(modinGroup, 0, 0)
        layout.addWidget(modoutGroup, 1, 0)
        self.setLayout(layout)

        self.setWindowTitle("MOD calculator pyqt5, v {}".format(gui_version))

    #        self.show()

    # calculation callback
    def calc_cmd(self):
        '''callback for calculate button '''
        o2pct = float(self.o2pctEdit.text())
        ppo2 = float(self.ppo2Edit.text())
        mod_m = mod_calc(ppo2, o2pct)
        self.modout.setText("{:.1f}".format(mod_m))
        print("calc_cmd o2pct= {} ppo2= {} => mod= {}".format(o2pct, ppo2, mod_m))

        pass

    def mix_change(self, index):
        print("mix_change: {}".format(index))
        o2mixes = [21, 21, 32, 50, 100]
        mixo2 = o2mixes[index]
        self.o2pctEdit.setText("{}".format(mixo2))

        pass


# main window loop starts now
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = mod_gui_win()
    window.show()
    sys.exit(app.exec_())

# done
