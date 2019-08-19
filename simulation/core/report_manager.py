"""
Report generator for producing pdf files containing results of multiple
simulation runs.
"""
import os
import glob
import pylatex as pl
from pylatex.utils import NoEscape, bold
from matplotlib import pyplot as plt


def mono(s):
    return NoEscape(r'\texttt{' + s + '}')


def tiny(s):
    return NoEscape(r'\scriptsize{' + s + '}')


class ReportManager:
    def __init__(self, run_title="Experiment", output_dir="../../output"):
        self.m_title = run_title
        self.m_run_prefix = "run"
        self.m_comment = "none"
        self.m_output_dir = os.path.abspath(
            os.path.join(os.path.split(__file__)[0], output_dir))
        self.m_output_index = 1

        geometry_options = {"margin": "0.5in"}
        self.m_doc = pl.Document("run-summary", document_options="landscape",
                                 geometry_options=geometry_options)

        self.prepare_output_dir()

    @staticmethod
    def make_dir(dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def prepare_output_dir(self):
        self.make_dir(self.m_output_dir)
        files = glob.glob(self.m_output_dir+"/*")
        for f in files:
            os.remove(f)

    def output_png(self):
        """
        Returns file name to store pyplot figure.
        """
        return '{}/{}-{:02d}.png'.format(self.m_output_dir, self.m_run_prefix,
                                         self.m_output_index)

    def write_report(self, parameter_tuple=None, slide_title=None):
        """
        Append single page to PDF report (in memory).
        The page will contain a table with current list of parameters, and single
        image which is currently in pyplot.
        """
        doc = self.m_doc
        if slide_title:
            doc.append(slide_title)
        else:
            doc.append(self.m_title)

        doc.append(pl.VerticalSpace("2cm"))
        doc.append("\n")
        self.create_parameter_minipage(parameter_tuple)
        self.create_figure_minipage()
        doc.append(pl.NewPage())
        self.m_output_index += 1

    def create_parameter_minipage(self, parameter_tuple):
        """
        Creates minipage with latex table
        """
        doc = self.m_doc
        with doc.create(pl.MiniPage(width=r"0.25\textwidth",
                                    height=r"0.25\textwidth",
                                    content_pos='t')):
            if not parameter_tuple:
                doc.append(pl.HorizontalSpace("2cm"))
                return
            with doc.create(pl.Tabular('l l', row_height=0.8)) as table:
                for l in parameter_tuple:
                    if len(l[1]):
                        myfont = [mono, tiny]
                    else:
                        myfont = [mono, tiny, bold]
                        table.add_row(" ", " ", mapper=myfont)  # empty row

                    table.add_row(l[0], l[1], mapper=myfont)

    def create_figure_minipage(self):
        """
        Create minipage with single figure which is currently in pyplot memory
        """
        doc = self.m_doc
        plt.savefig(self.output_png())
        with doc.create(pl.MiniPage(width=r"0.75\textwidth",
                                    height=r"0.25\textwidth",
                                    content_pos='t')):
            doc.append(pl.StandAloneGraphic(self.output_png(),
                image_options=NoEscape(r'width=0.99\textwidth')))
            doc.append("\n")

    def generate_pdf(self):
        """
        Write all pages in single pdf file.
        """
        filepath = os.path.join(self.m_output_dir, self.m_run_prefix+"-summary")
        self.m_doc.generate_pdf(clean_tex=False, filepath=filepath)

