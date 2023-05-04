"""Module responsible for the core logic of the forward model."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import os
import functools

from forward_model.params import read_iop_params, read_iops
from forward_model.samples import *
from forward_model.plots import *
from forward_model.widgets import build_widgets
from forward_model.components import *
from forward_model.colours import cs_srgb as cs

def make_box_layout():
     return widgets.Layout(
        border='solid 1px black',
        margin='0px 10px 10px 0px',
        padding='5px 5px 5px 5px'
     )

class ForwardModel(widgets.HBox):
     
    def __init__(self):
        # initialise the super class
        super().__init__()

        # set axis y-limits
        self.axis_limits = {}
        self.axis_limits["rrs_ylimits"] = [0.0, 0.05]
        self.axis_limits["absorption_ylimits"] = [0.0, 5]
        self.axis_limits["scatter_ylimits"] = [-4, 2]
        
        # read static values
        self.conditions = {}
        self.conditions["params"] = read_iop_params()
        self.conditions["wavelengths"],\
          self.conditions["abs_coeff_water"],\
          self.conditions["abs_increment"],\
          self.conditions["scattering_coefficient"] = read_iops()
        self.conditions["sample_files"], self.conditions["rrs_samples"] = read_rrs_samples(self.conditions["params"])
        self.conditions["saved_samples"] = self.conditions["wavelengths"]*0.0
        self.conditions["user_files"], self.conditions["user_samples"] = read_rrs_user(self.conditions["params"])
        self.conditions["chl_default"] = 1
        self.conditions["nap_default"] = 1
        self.conditions["cdom_default"] = 1

        # set colours for sample spectra
        cmf_wavs = np.loadtxt(os.path.join(os.getcwd(), 'forward_model', 'cie-cmf.txt'), usecols=(0))
        self.sample_plot_colours = []
        for sample in self.conditions["rrs_samples"]:
            interp_sample = np.interp(cmf_wavs, np.array([ii[0] for ii in sample]), 
                                     np.array([ii[1] for ii in sample]))
            self.sample_plot_colours.append(cs.spec_to_rgb(interp_sample, out_fmt='html'))
        
        # setup output streams for plots
        self.saved_spectra = self.conditions["wavelengths"]*0.0
        self.output_vals = widgets.Output()
        self.output_spectral_rrs = widgets.Output()
        self.output_spectral_absorption = widgets.Output()
        self.output_spectral_backscatter = widgets.Output()

        # define initial conditions
        components = calc_components(
            self.conditions["wavelengths"],
            self.conditions["params"],
            self.conditions["abs_coeff_water"],
            self.conditions["abs_increment"],
            self.conditions["scattering_coefficient"],
            self.conditions["chl_default"],
            self.conditions["nap_default"],
            self.conditions["cdom_default"])

        # define parameters for "inputs" plot
        set_input_plot(self)
  
        # define parameters for "spectral" plots
        set_spectral_rrs_plot(self, self.conditions["wavelengths"], components)
        set_spectral_absorption_plot(self, self.conditions["wavelengths"], components)
        set_spectral_backscatter_plot(self, self.conditions["wavelengths"], components)

        # define widgets
        chl_slider, nap_slider, cdom_slider, rrs_samples, user_samples, \
            saved_samples, save_spectra_button, options_fQ, options_two_species = build_widgets(self)

        # functionality for the save spectra button
        save_spectra_button.on_click(self.save_spectra)

        # set control panel
        self.controls = widgets.VBox([
            chl_slider, 
            nap_slider, 
            cdom_slider,
            self.output_vals,
            rrs_samples,
            user_samples,
            save_spectra_button,
            saved_samples
        ])

        self.spectral_plots = widgets.VBox([self.output_spectral_rrs,
                                            self.output_spectral_absorption,
                                            self.output_spectral_backscatter])

        # define layouts
        self.controls.layout = make_box_layout()
        out_box = widgets.Box([self.spectral_plots])
        self.spectral_plots.layout = make_box_layout()
        
        # add to children
        self.children = [self.controls, self.spectral_plots]
      
        # observe spectra
        chl_slider.observe(self.update_model, 'value')
        nap_slider.observe(self.update_model, 'value')
        cdom_slider.observe(self.update_model, 'value')

        # show sample spectra
        rrs_samples.observe(self.show_sample_plots, 'value')

        # show user spectra
        user_samples.observe(self.show_user_plots, 'value')

        # show saved spectra
        saved_samples.observe(self.show_saved_plots, 'value')

    def save_spectra(self, arg):
        """Define saved spectra"""

        components = calc_components(
            self.conditions["wavelengths"],
            self.conditions["params"],
            self.conditions["abs_coeff_water"],
            self.conditions["abs_increment"],
            self.conditions["scattering_coefficient"],
            self.children[0].children[0].value,
            self.children[0].children[1].value,
            self.children[0].children[2].value)

        self.conditions["saved_samples"] = components["rrs"]
        
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
          "Rrs_samples", "Rrs_user_last.txt"),"w") as saved_spectra_file:
            saved_spectra_file.write(f"# Wavelength (nm), Rrs\n")
            for wavelength, rrs in zip(self.conditions["wavelengths"], components["rrs"]):
                saved_spectra_file.write(f"{str(int(wavelength))},{str(rrs)}\n")
        
    def update_model(self, change):
        """Draw line in plot"""
        chl_val = self.children[0].children[0].value
        nap_val = self.children[0].children[1].value
        cdom_val = self.children[0].children[2].value
        TSM = nap_val + chl_val * float(self.conditions["params"]["Constituents"]["Chl2DW"])

        components = calc_components(
            self.conditions["wavelengths"],
            self.conditions["params"],
            self.conditions["abs_coeff_water"],
            self.conditions["abs_increment"],
            self.conditions["scattering_coefficient"],
            chl_val,
            nap_val,
            cdom_val)

        self.line1a.set_ydata([np.log10(chl_val), np.log10(nap_val), np.log10(cdom_val)])
        self.line1b.set_ydata(np.log10(TSM))

        self.line2a.set_ydata(components["rrs"])

        self.line3a.set_ydata(components["total_absorption"])
        self.line3b.set_ydata(components["aw"])
        self.line3c.set_ydata(components["aph"])
        self.line3d.set_ydata(components["aCDOM"])
        self.line3e.set_ydata(components["aNAP"])

        self.line4a.set_ydata(np.log10(components["total_backscatter"]))
        self.line4b.set_ydata(np.log10(components["bbw"]))
        self.line4c.set_ydata(np.log10(components["bbph"]))
        self.line4d.set_ydata(np.log10(components["bbpNAP"]))

    def show_sample_plots(self, change):

        if change.new:
            self.rrs_samples = [None] * np.shape(self.conditions["rrs_samples"])[0]
            for ii in range(np.shape(self.conditions["rrs_samples"])[0]):
                self.rrs_samples[ii], = self.ax_rrs.plot(
                    self.conditions["rrs_samples"][ii,:,0],
                    self.conditions["rrs_samples"][ii,:,1],
                    color=self.sample_plot_colours[ii], linestyle='--')
        else:
            for item in self.rrs_samples:
                item.set_ydata(None)

    def show_user_plots(self, change):
        if change.new:
            self.user_samples = [None] * np.shape(self.conditions["user_samples"])[0]
            for ii in range(np.shape(self.conditions["user_samples"])[0]):
                if "L8" in self.conditions["user_files"][ii]:
                    plot_col = "r"
                    marker= "^"
                    markersize=10
                elif "S2" in self.conditions["user_files"][ii]:
                    plot_col = "b"
                    marker= "s"
                    markersize=10
                elif "last" in self.conditions["user_files"][ii]:
                    plot_col = "0.5"
                    marker= "."
                    markersize=1
                else:
                    plot_col = "m"
                    marker= "o"
                    markersize=10

                self.user_samples[ii] = self.ax_rrs.scatter(
                    self.conditions["user_samples"][ii,:,0],
                    self.conditions["user_samples"][ii,:,1],
                    s=markersize, color=plot_col, marker=marker)
        else:
            for item in self.user_samples:
                item.set_visible(False)

    def show_saved_plots(self, change):

        if change.new:
            self.saved_samples = np.shape(self.conditions["saved_samples"])[0]
            self.saved_samples = self.ax_rrs.plot(self.conditions["wavelengths"], self.conditions["saved_samples"],
                                 color='0.5', linestyle='--')
        else:
            for item in self.saved_samples:
                item.set_ydata(None)