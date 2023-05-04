"""Module responsible for reading in Rrs samples."""

import glob
import numpy as np
import pathlib
import os

def read_rrs_samples(params):

    # read Rrs samples
    resolved_rrs_path=os.path.join(pathlib.Path(__file__).parent.resolve(), params["Rrs_samples"]["sample_dir"],'*sample*.txt')
    sample_files = glob.glob(resolved_rrs_path)
    rrs_samples = []
    for sample_file in sample_files:
        this_sample = np.genfromtxt(sample_file, comments="#", delimiter=',', dtype=float)
        this_sample[this_sample <0] = np.nan
        rrs_samples.append(this_sample)

    rrs_samples = np.array(rrs_samples)

    return sample_files, rrs_samples

def read_rrs_user(params):

    # read Rrs samples
    resolved_rrs_path=os.path.join(pathlib.Path(__file__).parent.resolve(), params["Rrs_samples"]["sample_dir"],'*user*.txt')
    user_files = glob.glob(resolved_rrs_path)
    rrs_users = []
    for user_file in user_files:
        this_user_sample = np.genfromtxt(user_file, comments="#", delimiter=',', dtype=float)
        this_user_sample[this_user_sample <0] = np.nan
        rrs_users.append(this_user_sample)

    rrs_users = np.array(rrs_users)

    return user_files, rrs_users