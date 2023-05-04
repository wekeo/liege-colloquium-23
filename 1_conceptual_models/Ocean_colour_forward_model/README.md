# Ocean Colour Forward Model

Changes in the concentration of chlorophyll (Chl), coloured dissolved organic matter (CDOM) and non-algae particles (NAP, e.g. sediment) in water have a marked effect on its colour. These changes are measurable by us, as observers, and by ocean colour satellites. When we know the concentrations of these consituents, **forward modelling** allows us to simulate the spectrally dependant inherent optical properties of the consituents (primarily absorption and scattering), and in turn determine the reflectance, the apparent optical property we typically measure from space and with in situ radiometry instruments.

In this module we provide a Python based forward model based on three consituents; Chl, CDOM (measured at 443 nm) and NAP. By varying these quantities we are able to see the resulting changes in the absorption (*a*), backscattering (*b*) and remote sensing reflectance (*Rrs*) spectra observed at the ocean surface. This can give an understanding of how the ocean colour signal can vary, how sensitive it is to changes in different constituents, and how it might be exploited through multi and hyperspectral satellite measurements and geophysical retrieval algorithms.

The model is consists of a modular toolkit (written in Python) and a simple Jupyter Notebook front-end implementation which allows it to be run "live" via a dashboard of widgets. We recommend installing the package using the Anaconda package manager. Step-by-step installation instructions are included below.

## License
 
This code is licensed under an MIT license. See file ../LICENSE.txt for details on 
the usage and distribution terms. No dependencies are distributed as part of this 
package. Copyright RBINS/EUMETSAT 2022.

All product names, logos, and brands are property of their respective owners. 
All company, product and service names used in this website are for identification 
purposes only.

## Authors

* [**Kevin Ruddick**](mailto://kruddick@naturalsciences.be) - [RBINS](https://www.naturalsciences.be/)
* [**Ben Loveday**](mailto://ops@eumetsat.int) - [EUMETSAT](http://www.eumetsat.int)
* [**Hayley Evers-King**](mailto://ops@eumetsat.int) - [EUMETSAT](http://www.eumetsat.int)

### Additional authors

* **Christian Hill** - development of the colours.py module. Please see module for more information.

## Prerequisites

You will require `Jupyter Notebook` to run this code. We highly recommend that you install 
the latest [Anaconda Python distribution](https://www.anaconda.com/) for your 
operating system. Anaconda Python distributions include Jupyter Notebook.

## Installation

1. **Cloning/Downloading the code**

The simplest and best way to install these packages is via Git. Users can clone this 
repository by running the following commands from either their [terminal](https://tinyurl.com/2s44595a) 
(on Linux/OSx), or from the [Anaconda prompt](https://docs.anaconda.com/anaconda/user-guide/getting-started/). 

`git clone https://gitlab.com/benloveday/oc_forward_model.git`

This will make a local copy of all the relevant files.

You can usually find your terminal in the start menu of most Linux distributions 
and in the Applications/Utilities folder  on OSx. Alternatively, you should be 
able to find/open your Anaconda Powershell prompt from your start menu (or dock, or via running 
the Anaconda Navigator). Once you have opened a terminal/prompt, you should navigate 
to the directory where you want to put the code. Once you are in the correct directory, 
you should run the following command;

Alternatively, you can download the package using the download icon (down arrow) on the top right of this page. *Note, we highly recommend you put this small package somewhere easy to find on your file manage, e.g. the Desktop, or Anaconda may not be able to find it*

2. **Setting up the code environment**

Inside the downloaded folder you will find a file called `environment.yml`. This contains all the information you will need to set up the necessary code environment to run the package. You can use this file in two ways.

If you are comfortable with the command line (terminal or Anaconda Prompt) you can navigate to the package folder and use the following commands;

`conda env create -f environment.yml` \
`conda activate oc_forward_model` \

This will create the necessary python environment, load it and launch jupyter notebook.

If you prefer to use the Anaconda Navigator GUI, you can import the environment by accessing the `Environment` tab on the left hand side of the Navigator home screen, and the use the `import` button to browse to the downloaded environment.yml file. This will create a new environment called 'oc_forward_model' in the drop down list. You should select this environment. *Note: you may need to re-select this each time you open the Anaconda Navigator*

3. **Running Jupyter Notebook and the code itself**

If you are working from the terminal you can use the following command to launch Jupyter Notebook

`jupyter notebook` or `jupyter-notebook` (depending on your operating system)

This should open Jupyter Notebook in a browser window. On occasion, Jupyter may not
be able to open a window and will give you a URL to past in your browser. Please do
so, if required.

*Note: Jupyter Notebook is not able to find modules that are 'above' it in a directory 
tree, and you will unable to navigate to these. So make sure you run the line above 
from the correct directory!*

If you are using the Anaconda Navigator you can click the Jupyter Notebook "launch" button and then navigate to where you installed the code.

You can then browse you file system in the Jupyter Notebook window to find the `Run_model.ipynb` notebook.

## Potential development work

There are no guarantees the following will occur, but I/we remain open to suggestions and collaborations. Please raise an issue on this repository if you want to comment on code improvements/expansion.

* Add Bernard at al. effective diamater and dual algal population models.
* Homogenise Ruddick and Bernard LUTs...possible or dual model?
* Add OLCI, MSI, FCI "extractions" at specified wavelengths and with relevant SRFs
* Add "idealised" atmosphere addition? RT-TOV is a possibility.
* Add BRDF dependance function for anistropy.
