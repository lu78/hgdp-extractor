#!/usr/bin/env python

import unittest
import commands
import difflib
import filecmp
from datetime import datetime
import time
import logging

class base_hgdpextractor(unittest.TestCase):
    """
    This module tests the script hgdp_snp_extractor.

    all the test cases derived from this module (e.g. test_european_chr1) 
    will execute the same tests.
    
     """
    # The following variables should be common for all the tests:
    _command_executed = False
    logging.basicConfig(level = logging.DEBUG)
    basedir = '/home/gioby/Data/HGDP/'
    samplesfile = basedir + 'Annotations/samples_subset.csv'
    genotypes_by_chr_dir = basedir + 'Genotypes_by_chr/'
    
    # The following variables should be redefined in every subclassed test:
    continent = ''
    chromosome = ''
    outputfile = basedir + 'Results/hgdp_chr%s_%s.geno'
    expected_outputfile = ''
    output = datetime.now()
    
    def _launch_python_command(self, command):
        """
        This function substitute an hypothetical setUpAll method 
        (if only unittest supported this)

        If this is the first test ran, run the python command; otherwise, pass
        """
        output = commands.getoutput(self.python_command)
        self._command_executed = 1
        logging.debug('command executed:\n%s' % self.python_command)
        return output

    def setUp(self):
        """
        launch the python script hgdp_snp_extractor
        """
        self.python_command = 'python hgdp_snp_extractor.py -c %s -y %s -g %s -o %s' % (self.continent, 
                                                self.chromosome, self.genotypes_by_chr_dir,
                                                self.outputfile)
        if not self._command_executed:
            self.output = self._launch_python_command(self.python_command)
        logging.debug(self.output)

    def test_outputfile_is_expected(self):
        """Checks that the output is equal to the expected"""
        out = self.outputfile
        expected = self.expected_outputfile
        
        logging.debug( 'output ' + self.output)
        # basic comparison #TODO: use difflib module
        filecmp.cmp(out, expected, shallow=False)


class test_europen_chr1(base_hgdpextractor):
    """test extraction of chromosome 1 from europeans"""

    continent = 'Europe'
    chromosome = '1'

    outputfile = ''
    expected_output = '/home/gioby/Data/HGDP/Test/chr1_30_filtered_europe.txt:'

   

        
