"""Module responsible for building the plots."""
import numpy as np
import matplotlib.pyplot as plt

def set_input_plot(self):

    self.x = [1, 3, 5, 7]
    self.y = [np.log10(self.conditions["chl_default"]), 
              np.log10(self.conditions["nap_default"]), 
              np.log10(self.conditions["cdom_default"]),
              np.log10(self.conditions["nap_default"] 
                       + self.conditions["chl_default"] 
                       * float(self.conditions["params"]["Constituents"]["Chl2DW"]))]

    with self.output_vals:
        self.fig1, self.ax1 = plt.subplots(constrained_layout=True, figsize=(3,2))
        self.line1a, = self.ax1.plot(self.x[0:3], self.y[0:3], "o", linewidth=0, color="r")
        self.line1b, = self.ax1.plot(self.x[3], self.y[3], "o", linewidth=0, color="0.5")
        self.ax1.set_ylabel('$Concentration$')
        self.ax1.set_xlim([0, 8])
        self.ax1.set_ylim([-3, 4])
        self.ax1.set_yticks(range(-3, 4))
        self.ax1.set_yticklabels([10**exp for exp in range(-3, 4)])
        self.ax1.set_xticks(self.x)
        self.ax1.set_xticklabels(["[Chl-a]\n$[mg.m^{-3}]$",
                                  "NAP\n$[g.m^{-3}]$",
                                  "CDOM$_{443}$\n$[m^{-1}]$",
                                  "TSM\n$[g.m^{-3}]$"], fontsize=8)
        plt.show()

    self.fig1.canvas.toolbar_visible = False
    self.fig1.canvas.resizable = False
    self.fig1.canvas.header_visible = False
    self.ax1.grid(True)

def set_spectral_rrs_plot(self, wavs, components):

        with self.output_spectral_rrs:
            self.fig2, self.ax_rrs = plt.subplots(constrained_layout=True, figsize=(6,2))
            self.line2a, = self.ax_rrs.plot(wavs, components["rrs"], 'k')
            self.ax_rrs.set_xlabel('$Wavelength \: [nm]$')
            self.ax_rrs.set_ylabel('$R_{rs} \: [sr^{-1}]$')
            self.ax_rrs.set_xlim([min(wavs), max(wavs)])
            self.ax_rrs.set_ylim(self.axis_limits["rrs_ylimits"])
            leg = plt.legend([self.line2a], ['$R_{rs}$'], fontsize=6)
            leg.get_frame().set_linewidth(0.0)
            plt.show()

        self.fig2.canvas.toolbar_position = 'bottom'
        self.fig2.canvas.resizable = False
        self.fig2.canvas.header_visible = False
        self.ax_rrs.grid(True)

def set_spectral_absorption_plot(self, wavs, components):

        self.wavs = range(0,700)
        self.rrs = np.zeros(np.shape(self.wavs))

        with self.output_spectral_absorption:
            self.fig3, self.ax_abs = plt.subplots(constrained_layout=True, figsize=(6,2))

            self.line3a, = self.ax_abs.plot(wavs, components["total_absorption"], 'k')
            self.line3b, = self.ax_abs.plot(wavs, components["aw"], 'r')
            self.line3c, = self.ax_abs.plot(wavs, components["aph"], 'b')
            self.line3d, = self.ax_abs.plot(wavs, components["aCDOM"], 'g')
            self.line3e, = self.ax_abs.plot(wavs, components["aNAP"], '0.25')

            self.ax_abs.set_xlabel('$Wavelength \: [nm]$')
            self.ax_abs.set_ylabel('$Absorption \: [m]^{-1}$')
            self.ax_abs.set_xlim([min(wavs), max(wavs)])
            self.ax_abs.set_ylim(self.axis_limits["absorption_ylimits"])
            leg = plt.legend([self.line3a,
                              self.line3b,
                              self.line3c,
                              self.line3d,
                              self.line3e],
                             ['total absorption', 'aw', 'aph', 'aCDOM', 'aNAP'],
                             fontsize=6)
            
            leg.get_frame().set_linewidth(0.0)
            plt.show()

        self.fig3.canvas.toolbar_position = 'bottom'
        self.fig3.canvas.resizable = False      
        self.fig3.canvas.header_visible = False
        self.ax_abs.grid(True)

def set_spectral_backscatter_plot(self, wavs, components):

        with self.output_spectral_backscatter:
            self.fig4, self.ax_scat = plt.subplots(constrained_layout=True, figsize=(6,2))

            self.line4a, = self.ax_scat.plot(wavs, np.log10(components["total_backscatter"]), 'k')
            self.line4b, = self.ax_scat.plot(wavs, np.log10(components["bbw"]), 'r')
            self.line4c, = self.ax_scat.plot(wavs, np.log10(components["bbph"]), 'g')
            self.line4d, = self.ax_scat.plot(wavs, np.log10(components["bbpNAP"]), 'b')

            self.ax_scat.set_xlabel('$Wavelength \: [nm]$')
            self.ax_scat.set_ylabel('$Backscatter \: [m^{-1}]$')
            self.ax_scat.set_xlim([min(wavs), max(wavs)])
            self.ax_scat.set_ylim(self.axis_limits["scatter_ylimits"])
            self.ax_scat.set_yticks(range(self.axis_limits["scatter_ylimits"][0], self.axis_limits["scatter_ylimits"][1]))
            self.ax_scat.set_yticklabels([10**exp for exp in range(self.axis_limits["scatter_ylimits"][0],
                                                               self.axis_limits["scatter_ylimits"][1])])
            leg = plt.legend([self.line4a,
                              self.line4b,
                              self.line4c,
                              self.line4d],
                             ['total backscatter', 'bbw', 'bbph', 'bbpNAP'],
                             fontsize=6)
            
            leg.get_frame().set_linewidth(0.0)
            plt.show()
            
        self.fig4.canvas.toolbar_position = 'bottom'
        self.fig4.canvas.resizable = False
        self.fig4.canvas.header_visible = False
        self.ax_scat.grid(True)
