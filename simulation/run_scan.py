"""
Run consecutive simulations to scan sample parameter influence.
"""
from core.report_manager import ReportManager
import numpy as np
from run_simulation import run_single
from core.utils import load_setup
import os


def scan_grating_height(exp_config, sample_config, report_manager):
    report_manager.m_title = "Grating height scan"
    for value in np.linspace(180.0, 220.0, 11):
        sample_config["grating_height"] = value
        run_single(exp_config, sample_config, report_manager)


def scan_grating_period(exp_config, sample_config, report_manager):
    report_manager.m_title = "Grating period scan"
    for value in np.linspace(820.0, 840.0, 11):
        sample_config["grating_period"] = value
        run_single(exp_config, sample_config, report_manager)


def single_shot(exp_config, sample_config, report_manager):
    report_manager.m_title = "Single shot"
    run_single(exp_config, sample_config, report_manager)


def run_scan(exp_config, sample_config, report_manager):
    # scan_grating_height(exp_config, sample_config, report_manager)
    scan_grating_period(exp_config, sample_config, report_manager)


def main():
    output = os.path.abspath(os.path.join(os.path.split(__file__)[0], "../output"))
    report_manager = ReportManager(output)

    exp_config = load_setup("experiments.json", "exp3")
    sample_config = load_setup("gratings.json", "sinus")

    run_scan(exp_config, sample_config, report_manager)

    report_manager.generate_pdf()
    print("Terminated successfully")


if __name__ == '__main__':
    main()
