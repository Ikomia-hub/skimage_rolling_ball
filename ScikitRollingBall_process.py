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

from ikomia import core, dataprocess
import copy
from skimage import (
    data, restoration, util
)


# --------------------
# - Class to handle the process parameters
# - Inherits PyCore.CProtocolTaskParam from Ikomia API
# --------------------
class ScikitRollingBallParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        self.combo_model = "Dark"
        self.radius = 10
        self.kernel_choice = "ball_kernel"
        self.kernel_x = 10
        self.kernel_y = 10

    def setParamMap(self, param_map):
        self.combo_model = param_map["combo_model"]
        self.radius = int(param_map["radius"])
        self.kernel_choice = param_map["kernel_choice"]
        self.kernel_x = int(param_map["kernel_x"])
        self.kernel_y = int(param_map["kernel_y"])

    def getParamMap(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        param_map = core.ParamMap()
        param_map["combo_model"] = self.combo_model
        param_map["radius"] = str(self.radius)
        param_map["kernel_choice"] = self.kernel_choice
        param_map["kernel_x"] = str(self.kernel_x)
        param_map["kernel_y"] = str(self.kernel_y)
        return param_map


# --------------------
# - Class which implements the process
# - Inherits PyCore.CProtocolTask or derived from Ikomia API
# --------------------
class ScikitRollingBallProcess(core.CWorkflowTask):

    def __init__(self, name, param):
        core.CWorkflowTask.__init__(self, name)

        # Add input/output of the process here
        self.addInput(dataprocess.CImageIO())
        self.addOutput(dataprocess.CImageIO())
        self.addOutput(dataprocess.CImageIO())

        # Create parameters class
        if param is None:
            self.setParam(ScikitRollingBallParam())
        else:
            self.setParam(copy.deepcopy(param))

    def getProgressSteps(self, eltCount=1):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 3

    def run(self):
        # Core function of your process
        # Call beginTaskRun for initialization
        self.beginTaskRun()

        # Get input
        input_img = self.getInput(0)

        # Verification if the input is empty
        if not input_img.isDataAvailable():
            raise ValueError("your input is empty, restart the task")

        # Get output
        output_img = self.getOutput(0)
        output_bck = self.getOutput(1)

        # Get parameters
        param = self.getParam()
        print(param.combo_model)
        print("Start Rolling ball...")
        if param.combo_model == "Dark":
            image = input_img.getImage()
            if param.kernel_choice == "ball_kernel":
                if len(image.shape) < 3:
                    background = restoration.rolling_ball(image, radius=param.radius)
                else:
                    raise ValueError(
                        "the choice of kernel_ball is not suitable for a color image, choose ellipsoid_kernel")
            else:
                normalized_radius = param.radius / 255
                # testing the color of the image
                if len(image.shape) < 3:
                    kernel = restoration.ellipsoid_kernel((param.kernel_x, param.kernel_y), normalized_radius * 2)
                else:
                    kernel = restoration.ellipsoid_kernel((1, param.kernel_x, param.kernel_y), normalized_radius)

                background = restoration.rolling_ball(image, kernel=kernel)

            # Step progress bar:
            self.emitStepProgress()
            filtered_image = image - background
            # Step progress bar:
            self.emitStepProgress()
            output_img.setImage(filtered_image)
            output_bck.setImage(background)
        else:
            image = input_img.getImage()
            image_inverted = util.invert(image)

            if param.kernel_choice == "ball_kernel":
                background_inverted = restoration.rolling_ball(image_inverted, radius=param.radius)
            else:
                normalized_radius = param.radius / 255
                kernel = restoration.ellipsoid_kernel((param.kernel_x, param.kernel_y), normalized_radius * 2)
                background_inverted = restoration.rolling_ball(image_inverted, kernel=kernel)

            # Step progress bar:
            self.emitStepProgress()
            filtered_image_inverted = image_inverted - background_inverted
            filtered_image = util.invert(filtered_image_inverted)
            background = util.invert(background_inverted)
            # Step progress bar:
            self.emitStepProgress()
            output_img.setImage(filtered_image)
            output_bck.setImage(background)

        # Step progress bar:
        self.emitStepProgress()

        # Call endTaskRun to finalize process
        self.endTaskRun()


# --------------------
# - Factory class to build process object
# - Inherits PyDataProcess.CProcessFactory from Ikomia API
# --------------------
class ScikitRollingBallProcessFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "ScikitRollingBall"
        self.info.shortDescription = "The rolling-ball algorithm estimates the background intensity of " \
                                     "a grayscale image in case of uneven exposure"
        self.info.description = "The algorithm works as a filter and is quite intuitive. We think of the image as a " \
                                "surface that has unit-sized blocks stacked on top of each other in place of " \
                                "each pixel. The number of blocks, and hence surface height, is determined by the " \
                                "intensity of the pixel. To get the intensity of the background at a desired (pixel) " \
                                "position, we imagine submerging a ball under the surface at the desired position. " \
                                "Once it is completely covered by the blocks, the apex of the ball determines the " \
                                "intensity of the background at that position. We can then roll this ball around " \
                                "below the surface to get the background values for the entire image. This algorithm " \
                                "is recommended for grayscale images. However, if you want to apply it to color " \
                                "images, use the ellipsoid_kernel method."
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Background"
        self.info.version = "1.0.0"
        self.info.authors = "Sternberg, Stanley R."
        self.info.article = "Biomedical image processing."
        self.info.journal = " Computer 1: 22-34"
        self.info.year = 1983
        self.info.license = "MIT License"
        # URL of documentation
        self.info.documentationLink = "https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_rolling_ball.html"
        self.info.iconPath = "icons/scikit.png"
        # Code source repository
        self.info.repository = "https://github.com/Ikomia-dev/ScikitRollingBall"
        # Keywords used for search
        self.info.keywords = "scikit-image,rolling,ball,background,restoration"

    def create(self, param=None):
        # Create process object
        return ScikitRollingBallProcess(self.info.name, param)
