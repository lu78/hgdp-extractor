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
    basedir = '/home/gioby/Data/HGDP/'
    samplesfile = basedir + 'Annotations/samples_subset.csv'
    genotypes_by_chr_dir = basedir + 'Genotypes_by_chr/'
    
    # The following variables should be redefined in every subclassed test:
    continent = ''
    chromosome = ''
    outputfile = basedir + 'Results/hgdp_chr%s_%s.geno'
    expected_outputfile = ''
    output = datetime.now()
    
    # TODO: move call to commands.getoutput here? How to create global fixtures?
    # maybe it is better to use a flag (command._isset or similar)


    def setUp(self):
        """
        launch the python script hgdp_snp_extractor
        """
        python_command = 'python hgdp_snp_extractor -c %s -y %s -g %s -o %s' % (self.continent, 
                                                self.chromosome, self.genotypes_by_chr_dir,
                                                self.outputfile)
        logging.basicConfig(level = logging.DEBUG)
        self.output = commands.getoutput('python')
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

   

        
