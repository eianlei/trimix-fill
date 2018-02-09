#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# mod_gui_tk_pyqt5.py
# github project https://github.com/eianlei/trimix-fill/
#  this GUI uses function mod_calc() from tmx_calc.py
# use at your own risk, no guarantees, no liability!
#
# GUI to calculate MOD using pyqt5 and spinboxes
#  almost same UI design as mod_gui_tk.py done with tkinter, this is with pyqt5

gui_version = "0.1"

from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
                             QLabel, QLineEdit, QWidget, QPushButton, QSpinBox, QDoubleSpinBox)

# import modules, like PyQt5 stuff
from tmx_calc import mod_calc


# define the main window GUI objects and callbacks
class mod_gui_win(QWidget):
    def __init__(self):
        super(mod_gui_win, self).__init__()

        # GroupBox to hold input value Spinboxes and labels for them
        modinGroup = QGroupBox("Input values for calculating MOD")
        # a ComboBOx to quicky select O2% for some commong mixes
        modinmixLabel = QLabel("Std mixes:")
        modinComboBox = QComboBox()
        modinComboBox.addItem("air")
        modinComboBox.addItem("TMX 21/35")
        modinComboBox.addItem("EAN32")
        modinComboBox.addItem("EAN50")
        modinComboBox.addItem("OXYGEN")
        # callback for the value changes  mix_change()
        modinComboBox.activated.connect(self.mix_change)

        # input for O2%
        modin_o2pctLabel = QLabel("Oxygen %:")
        self.o2pctSpinBox = QSpinBox()
        self.o2pctSpinBox.setRange(12, 100)  # min 12%, max 100% O2
        self.o2pctSpinBox.setSingleStep(1)  # steps of 1
        self.o2pctSpinBox.setSuffix('%')  # show % suffix
        self.o2pctSpinBox.setValue(32)  # default is EAN32
        # recalculte MOD every time value changes calc_cmd()
        self.o2pctSpinBox.valueChanged.connect(self.calc_cmd)

        # input for ppO2
        modin_ppo2Label = QLabel("ppO2 in bar/ATA:")
        self.ppo2SpinBox = QDoubleSpinBox()
        self.ppo2SpinBox.setRange(1.0, 2.0)  # min 1.0, max 2.0
        self.ppo2SpinBox.setSingleStep(0.1)  # steps of 0.1
        self.ppo2SpinBox.setValue(1.4)  # most common ppO2
        # recalculte MOD every time value changes
        self.ppo2SpinBox.valueChanged.connect(self.calc_cmd)

        # EXIT button
        self.calc_btn = QPushButton('EXIT', self)
        self.calc_btn.clicked.connect(self.exit_button)

        # lay out all widgets to two grids
        # first the inputs
        modinLayout = QGridLayout()
        modinLayout.addWidget(modinmixLabel, 0, 0)
        modinLayout.addWidget(modinComboBox, 0, 1)
        modinLayout.addWidget(modin_o2pctLabel, 1, 0)
        modinLayout.addWidget(self.o2pctSpinBox, 1, 1)
        modinLayout.addWidget(modin_ppo2Label, 2, 0)
        modinLayout.addWidget(self.ppo2SpinBox, 2, 1)
        modinLayout.addWidget(self.calc_btn, 3, 0)
        modinGroup.setLayout(modinLayout)

        # output grid
        modoutGroup = QGroupBox("MOD result is")
        self.modout = QLineEdit()
        modoutLayout = QGridLayout()
        modoutLayout.addWidget(self.modout, 0, 0)
        unitLabel = QLabel("meters")
        modoutLayout.addWidget(unitLabel, 0, 1)
        modoutGroup.setLayout(modoutLayout)

        # lay out both sub grids to top level grid
        layout = QGridLayout()
        layout.addWidget(modinGroup, 0, 0)
        layout.addWidget(modoutGroup, 1, 0)
        self.setLayout(layout)

        # window title, and we are done
        self.setWindowTitle("MOD calculator pyqt5 SB, v {}".format(gui_version))

    # calculation callback, all spinboxes changing value
    def calc_cmd(self):
        '''callback for calculate button '''
        o2pct = self.o2pctSpinBox.value()
        ppo2 = self.ppo2SpinBox.value()
        mod_m = mod_calc(ppo2, o2pct)
        self.modout.setText("{:.1f}".format(mod_m))
        print("calc_cmd o2pct= {} ppo2= {} => mod= {}".format(o2pct, ppo2, mod_m))
        pass

    # callback when combobox modinComboBox changes value
    def mix_change(self, index):
        print("mix_change: {}".format(index))
        o2mixes = [21, 21, 32, 50, 100]
        mixo2 = o2mixes[index]
        self.o2pctSpinBox.setValue(mixo2)
        pass

    # EXIT button callback
    def exit_button(self):
        sys.exit()


# main window loop starts now
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = mod_gui_win()
    window.show()
    sys.exit(app.exec_())
# done, end of application
