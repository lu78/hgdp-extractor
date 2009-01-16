import unittest
import commands

class test_hgdpextractor(unittest.testcase):
    """ """
    samplesfile = '/home/gioby/Data/HGDP/Annotations/samples_subset.csv'
    

    def setUp(self):
        """
        launch the python script hgdp_snp_extractor
        """
        python_command = 'python hgdp_snp_extractor -c %s -y %s -g %s' %(self.continent, self.chromosome, self.genotypes_by_chr_dir)
        
        self.output = commands.getoutput('python')


class test_europen_chr1(test_hgdpextractor):

    def __init__(self):
        self.continent = 'Europe'
        self.chromosome = '1'
        self.genotypes_by_chr_dir = '' #TODO: define here
   

        
