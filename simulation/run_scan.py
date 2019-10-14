"""
Run consecutive simulations to scan sample parameter influence.
"""
from core.report_manager import ReportManager
import numpy as np
from run_simulation import run_single
from core.utils import load_setup
from tqdm import tqdm
import os


def scan_grating_height(exp_config, sample_config, report_manager):
    report_manager.m_title = "exp2/sinus height scan"
    for value in tqdm(np.linspace(225.0-20, 225.0+20, 3)):
        sample_config["grating_height"] = value
        run_single(exp_config, sample_config, report_manager, sim_title="height {:6.2f}".format(value))


def scan_grating_period(exp_config, sample_config, report_manager):
    report_manager.m_title = "Grating period scan"
    for value in np.linspace(834.0-5, 834.0+5, 11):
        sample_config["grating_period"] = value
        run_single(exp_config, sample_config, report_manager)

def scan_sample_rotation(exp_config, sample_config, report_manager):
    report_manager.m_title = "Grating period scan"
    for value in np.linspace(0.131-0.05, 0.131+0.05, 11):
        exp_config["sample_rotation"] = value
        run_single(exp_config, sample_config, report_manager)

def scan_spherical_r0(exp_config, sample_config, report_manager):
    report_manager.m_title = "Grating spherical r0"
    for value in np.linspace(225.0-40, 225+40.0, 41):
        sample_config["r0"] = value
        run_single(exp_config, sample_config, report_manager)

def scan_spherical_r0_height(exp_config, sample_config, report_manager):
    report_manager.m_title = "Grating spherical r0"
    for value in np.linspace(100.0, 300.0, 51):
        sample_config["r0_height"] = value
        run_single(exp_config, sample_config, report_manager)

def single_shot(exp_config, sample_config, report_manager):
    report_manager.m_title = "Sphericalsym, exp1"
    run_single(exp_config, sample_config, report_manager)


def run_scan(exp_config, sample_config, report_manager):
    scan_grating_height(exp_config, sample_config, report_manager)
    # scan_grating_period(exp_config, sample_config, report_manager)
    # scan_sample_rotation(exp_config, sample_config, report_manager)
    # scan_spherical_r0(exp_config, sample_config, report_manager)
    # scan_spherical_r0_height(exp_config, sample_config, report_manager)
    # single_shot(exp_config, sample_config, report_manager)

def main():
    output = os.path.abspath(os.path.join(os.path.split(__file__)[0], "../output"))
    report_manager = ReportManager(output)

    exp_config = load_setup("experiments.json", "exp1")
    sample_config = load_setup("gratings.json", "sphericalsym")

    run_scan(exp_config, sample_config, report_manager)

    report_manager.generate_pdf()
    print("Terminated successfully")


if __name__ == '__main__':
    main()
