<div align="center">
  <img src="https://raw.githubusercontent.com/Ikomia-hub/skimage_rolling_ball/main/icons/scikit.png" alt="Algorithm icon">
  <h1 align="center">skimage_rolling_ball</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/skimage_rolling_ball">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/skimage_rolling_ball">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/skimage_rolling_ball/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/skimage_rolling_ball.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

Use rolling-ball algorithm for estimating background intensity. 


![rolling ball](https://raw.githubusercontent.com/Ikomia-hub/skimage_rolling_ball/main/sample%20images/output.jpg)

## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow
```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_rolling_ball", auto_connect=True)

# Run on your image  
wf.run_on(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_rolling_ball/main/sample%20images/coins.png")

display(algo.get_output(0).get_image())
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.
- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).
- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters

- **combo_model** (str) default 'Dark': Background model choice 'Light' or 'Dark'
- **radius** (int) - default '10': Radius of a ball shaped kernel to be rolled/translated in the image.
- **kernel_choice** (str) - default 'ball_kernel': Kernel type. Other option: 'ellipsoid_kernel'
- **kernel_x** (int) - default '10'
- **kernel_y** (int) - default '10'

**Parameters** should be in **strings format**  when added to the dictionary.

```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_rolling_ball", auto_connect=True)


algo.set_parameters({
    "combo_model": "Light",
    "radius": "20",
    "kernel_choice": "ellipsoid_kernel",
    "kernel_x": "20",
    "kernel_y": "20",
})

# Run on your image  
wf.run_on(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_rolling_ball/main/sample%20images/coins.png")

display(algo.get_output(0).get_image())
```

## :mag: Explore algorithm outputs

Every algorithm produces specific outputs, yet they can be explored them the same way using the Ikomia API. For a more in-depth understanding of managing algorithm outputs, please refer to the [documentation](https://ikomia-dev.github.io/python-api-documentation/advanced_guide/IO_management.html).

```python
import ikomia
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_rolling_ball", auto_connect=True)

# Run on your image  
wf.run_on(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_rolling_ball/main/sample%20images/coins.png")

# Iterate over outputs
for output in algo.get_outputs():
    # Print information
    print(output)
    # Export it to JSON
    output.to_json()
```

## :fast_forward: Advanced usage 

The algorithm works as a filter and is quite intuitive. We think of the image as a surface that has unit-sized blocks stacked on top of each other in place of each pixel. 
The number of blocks, and hence surface height, is determined by the intensity of the pixel. 
To get the intensity of the background at a desired (pixel) position, we imagine submerging a ball under the surface at the desired position. 
Once it is completely covered by the blocks, the apex of the ball determines the intensity of the background at that position. We can then roll this ball around below the surface to get the background values for the entire image. This algorithm is recommended for grayscale images. However, if you want to apply it to color images, use the ellipsoid_kernel method.
