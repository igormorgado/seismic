import logging
import subprocess
import pandas
import io
import re

__author__ = 'Igor Morgado'
__version__ = "$Id: //vega/xp/src/base/miscg2/lscapi.py#1 $ $Author: imorgado $ $DateTime: 2016/01/29 10:11:12 $"
__email__ = "igormorgado@cgg.com"


log = logging.getLogger(__name__)


class LsCapi(object):
    """
    Encapsulate the calls to the lscapi utility.
    """



    def __init__(self, command_name="lscapi", longlist=None, vectors=None):
        self.command_name='lscapi'
        self.longlist = longlist
        self.vectors = vectors



    @property
    def general_args(self):
        """
        Build the general args used commonly on lscapi command line, based
        on properties on each class instance
        """
        args = []

        # CSV output is mandatory
        args += [ '-csv' ]

        if self.longlist:
            args += [ '-l' ]

        if self.vectors:
            args += [ '-showvectors' ]

        return args



    def evaluateError(self, msg):
        raise



    def query(self, dataset_name, filters=None, mapping=None):
        """
        Return a list of zero or more datasets
        :param dataset_name: name of dataset to be listed
        :filter: list of applied wildcard (*,?,[]) filters based on lscapi
                 syntax, valid filters are:
                        name
                        folder
                        class
                        subclass
                        creator
                        firstcreated
                        lastcreated
                        minsize
                        maxsize
                Example:
                    [ 'name="*stk*"', folder='/*/qc*/' ]
        :return: a dataframe with all objects
        """

        command_args = [self.command_name]
        command_args += self.general_args
        command_args += [dataset_name]

        if filters:
           for filter in filters:
               command_args += [ '-f' , filter ]

        # We should verify if dataset exists (that is, is a valid one)
        # Otherwise mapping does not work properly
        if mapping:
               command_args += [ '-map' , mapping ]
    
        log.debug("Executing: " + subprocess.list2cmdline(command_args))
        
        process = subprocess.Popen(
                command_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        (stdout, stderr) = process.communicate()
        status = process.wait()

        if status != 0:
            self.evaluateError()

        csv=io.StringIO(unicode(stdout,'utf-8'))
        df = pandas.read_csv(csv, sep=',', na_values = ['nan','NaN'] ) 

        return df



    def getGroupsAndSizes(self, dataset_name):
        """
        Perform a getGroupsAndSizes on the first key in the dataset.
        :param dataset_name: name of dataset to be listed
        :return: a dataframe with all objects
        """

        command_args  = [self.command_name]
        command_args += self.general_args
        command_args += ['-gas']
        command_args += [dataset_name]

        log.debug("Executing: " + subprocess.list2cmdline(command_args))
        
        process = subprocess.Popen(
                command_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        (stdout, stderr) = process.communicate()
        status = process.wait()

        if status != 0:
            self.evaluateError()

        csv=io.StringIO(stdout)
        df = pandas.read_csv(csv, sep=',', skip_blank_lines=True, quoting=2, skipinitialspace=True ) 

        return df



    def dataset_exists(self, dataset_name):
        """
        Return bool value if datasets exists or not
        :param dataset_name: name of dataset to be listed
        :return: a dataframe with all objects
        """

        command_args = [self.command_name]
        command_args += self.general_args 
        command_args += [ '-exists' ]
        command_args += [dataset_name]

        log.debug("Executing: " + subprocess.list2cmdline(command_args))
        
        process = subprocess.Popen(
                command_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        (stdout, stderr) = process.communicate()
        status = process.wait()

        if status != 0:
            self.evaluateError(stdout)

        if "answer=y" in stdout:
            return True
        else:
            return False



    def list_geovation_projects(self):
        """
        Return bool value if datasets exists or not
        :param dataset_name: name of dataset to be listed
        :return: a list with project names
        """

        dataset_name = "g::::"

        command_args  = [self.command_name]
        command_args += self.general_args
        command_args += [dataset_name]
        
        log.debug("Executing: " + subprocess.list2cmdline(command_args))
        
        process = subprocess.Popen(
                command_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        (stdout, stderr) = process.communicate()
        status = process.wait()

        if status != 0:
            self.evaluateError(stdout)

        csv=io.StringIO(stdout)
        df = pandas.read_csv(csv, sep=',', skip_blank_lines=True, quoting=2, skipinitialspace=True, skiprows=[ 1 ] ) 

        return df.ix[:,0].tolist()
    


    def list_geovation2_projects(self):
        """
        Return bool value if datasets exists or not
        :param dataset_name: name of dataset to be listed
        :return: a list with project names
        """

        dataset_name = "a::::"

        command_args = [self.command_name]
        command_args +=  self.general_args 
        command_args += [dataset_name]

        log.debug("Executing: " + subprocess.list2cmdline(command_args))
        
        process = subprocess.Popen(
                command_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        (stdout, stderr) = process.communicate()
        status = process.wait()

        if status != 0:
            self.evaluateError(stdout)

        csv=io.StringIO(stdout)
        df = pandas.read_csv(csv, sep=',', skip_blank_lines=True, quoting=2, skipinitialspace=True, skiprows=[ 1 ] ) 

        return df.ix[:,0].tolist()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    lscapi = LsCapi(longlist=True)

    #    print lscapi.list_geovation_projects()
    #
    #    print lscapi.list_geovation2_projects()
    #
    #    print lscapi.getGroupsAndSizes("a:::fcruz:/using_acorn")
    #
    #    print lscapi.dataset_exists("a:::fcruz:/using_acorn")
    #
    #    print lscapi.dataset_exists("a:::fcruz:/using_acor")
    #
    #    # There is a "problem" here, because if you specify the acorn dataset, it will
    #    # show a non csv parseable file
    #    # Need to check if the dataset name is a directory or a deterministic dataset

    #print lscapi.query("a:::fcruz")
    #print lscapi.query("a:::fcruz", filters=[ 'path=/bcp/' ])
    #print lscapi.query("a:::fcruz", filters=[ 'path=*/*j00*/' ])
    #print lscapi.query("a:::fcruz:/using_acorn")
    #print lscapi.query("select * from a:::fcruz:/using_acorn")
