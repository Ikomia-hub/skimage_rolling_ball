# Copyright (C) 2021 Ikomia SAS
# Contact: https://www.ikomia.com
#
# This file is part of the IkomiaStudio software.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ikomia import utils, core, dataprocess
from ikomia.utils import qtconversion
from skimage_rolling_ball.skimage_rolling_ball_process import RollingBallParam
# PyQt GUI framework
from PyQt5.QtWidgets import *


# --------------------
# - Class which implements widget associated with the process
# - Inherits PyCore.CProtocolTaskWidget from Ikomia API
# --------------------
class RollingBallWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = RollingBallParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()
        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.grid_layout)

        # Set widget layout
        self.setLayout(layout_ptr)
        # Creation widget background
        self.label_back = QLabel("Background color choice:")
        self.combo_model = QComboBox()
        self.combo_model.addItem("Dark")
        self.combo_model.addItem("Light")
        self.grid_layout.addWidget(self.label_back, 1, 0)
        self.grid_layout.addWidget(self.combo_model, 1, 1)
        self.combo_model.setCurrentText(self.parameters.combo_model)

        # Creation widget kernel_choice
        self.label_kernel_choice = QLabel("kernel-choice:")
        self.kernel_choice = QComboBox()
        self.kernel_choice.addItem("ball_kernel")
        self.kernel_choice.addItem("ellipsoid_kernel")
        self.grid_layout.addWidget(self.label_kernel_choice, 2, 0)
        self.grid_layout.addWidget(self.kernel_choice, 2, 1)
        self.kernel_choice.setCurrentText(self.parameters.kernel_choice)

        # link between widget and MethodChange
        self.kernel_choice.currentTextChanged.connect(self.on_method_change)

        # Creation radius widget
        self.label_radius = QLabel("radius:")
        self.radius = QSpinBox()
        self.radius.setMinimum(0)
        self.radius.setMaximum(200)
        self.radius.setValue(self.parameters.radius)

        # Creation widget kernel_ellipsoid x and y
        self.label_kernel_x = QLabel("kernel_x:")
        self.kernel_x = QSpinBox()
        self.kernel_x.setMinimum(0)
        self.kernel_x.setMaximum(255)
        self.kernel_x.setValue(self.parameters.kernel_x)

        self.label_kernel_y = QLabel("kernel_y:")
        self.kernel_y = QSpinBox()
        self.kernel_y.setMinimum(0)
        self.kernel_y.setMaximum(255)
        self.kernel_y.setValue(self.parameters.kernel_y)

        # applying the widget on the interface
        self.grid_layout.addWidget(self.label_kernel_x, 3, 0)
        self.grid_layout.addWidget(self.kernel_x, 3, 1)

        self.grid_layout.addWidget(self.label_kernel_y, 4, 0)
        self.grid_layout.addWidget(self.kernel_y, 4, 1)

        self.grid_layout.addWidget(self.label_radius, 3, 0)
        self.grid_layout.addWidget(self.radius, 3, 1)

        self.on_method_change()

    def on_method_change(self):

        if self.kernel_choice.currentText() == "ball_kernel":
            self.label_radius.show()
            self.radius.show()
            self.label_kernel_y.hide()
            self.label_kernel_x.hide()
            self.kernel_x.hide()
            self.kernel_y.hide()
        else:
            self.label_kernel_y.show()
            self.label_kernel_x.show()
            self.kernel_x.show()
            self.kernel_y.show()
            self.parameters.kernel_x = self.kernel_x.value()
            self.parameters.kernel_y = self.kernel_y.value()
            self.label_radius.hide()
            self.radius.hide()

    def onApply(self):
        # Apply button clicked slot
        # Get parameters from widget
        self.parameters.combo_model = self.combo_model.currentText()
        self.parameters.kernel_choice = self.kernel_choice.currentText()
        self.parameters.radius = self.radius.value()
        self.parameters.kernel_x = self.kernel_x.value()
        self.parameters.kernel_y = self.kernel_y.value()

        # Send signal to launch the process
        self.emitApply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits PyDataProcess.CWidgetFactory from Ikomia API
# --------------------
class RollingBallWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "skimage_rolling_ball"

    def create(self, param):
        # Create widget object
        return RollingBallWidget(param, None)
