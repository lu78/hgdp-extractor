import unittest
import commands
import difflib
import filecmp

class test_hgdpextractor(unittest.TestCase):
    """ """
    # The following variables should be common for all the tests:
    samplesfile = '/home/gioby/Data/HGDP/Annotations/samples_subset.csv'
    genotypes_by_chr_dir = '/home/gioby/Data/HGDP/Genotypes_by_chr'
    
    # The following variables should be redefined in every subclassed test:
    continent = ''
    chromosome = ''
    outputfile = ''
    expected_outputfile = ''
    

    def setUp(self):
        """
        launch the python script hgdp_snp_extractor
        """
        python_command = 'python hgdp_snp_extractor -c %s -y %s -g %s' %(self.continent, self.chromosome, self.genotypes_by_chr_dir)
        
        self.output = commands.getoutput('python')

    def test_outputfile_is_expected(self):
        """Checks that the output is equal to the expected"""
        out = self.outputfile
        expected = self.expected_outputfile
        
        # basic comparison #TODO: use difflib module
        filecmp.cmp(out, expected, shallow=False)

class test_europen_chr1(test_hgdpextractor):
    """test extraction of chromosome 1 from europeans"""

    continent = 'Europe'
    chromosome = '1'

    outputfile = ''
    expected_output = '/home/gioby/Data/HGDP/Test/chr1_30_filtered_europe.txt:'

   

        
