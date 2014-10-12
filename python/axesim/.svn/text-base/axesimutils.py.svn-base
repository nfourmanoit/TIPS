"""
$Revision: 1.2.2.1 $ $Date: 2009/09/21 15:11:35 $
Author: Martin Kuemmel (mkuemmel@stecf.org)
Affiliation: Space Telescope - European Coordinating Facility
WWW: http://www.stecf.org/software/slitless_software/axesim/
"""
import os
import os.path
import sys
import string

AXE_IMAGE_PATH   = './'
AXE_OUTPUT_PATH  = './'
AXE_CONFIG_PATH  = './'
AXE_SIMDATA_PATH = './'
AXE_OUTSIM_PATH  = './'

def get_environments():
    """
    Save environmental variables as global variables

    The function checks for the existence of the environmental
    variables which are used in axe to direct in/output.
    The values stored in the environmental variables are
    stored in global variables of the same name.
    """
    global AXE_IMAGE_PATH
    global AXE_OUTPUT_PATH
    global AXE_CONFIG_PATH
    global AXE_SIMDATA_PATH
    global AXE_OUTSIM_PATH
    global AXESIMBIN

    ret = 0

    if 'AXE_IMAGE_PATH' in os.environ:
        AXE_IMAGE_PATH = os.environ['AXE_IMAGE_PATH']
    if 'AXE_OUTPUT_PATH' in os.environ:
        AXE_OUTPUT_PATH = os.environ['AXE_OUTPUT_PATH']
    if 'AXE_CONFIG_PATH' in os.environ:
        AXE_CONFIG_PATH = os.environ['AXE_CONFIG_PATH']
    if 'AXE_SIMDATA_PATH' in os.environ:
        AXE_SIMDATA_PATH = os.environ['AXE_SIMDATA_PATH']
    if 'AXE_OUTSIM_PATH' in os.environ:
        AXE_OUTSIM_PATH = os.environ['AXE_OUTSIM_PATH']

    if 'axesim' in sys.modules:
        modfile = sys.modules['axesim'].__file__

    #AXESIMBIN = get_axesimbin()
    AXESIMBIN = os.path.abspath(os.path.join(os.path.dirname(modfile),'bin/'))

    return ret

def putCONF(name=None):
    """
    Sets the path to a file in the $AXE_CONFIG_PATH directory

    Appends the input parameter behind the content of the
    (gloal) variable 'AXE_CONFIG_PATH'. Checks for
    multiple directory indicators ('/') before returning
    the result

    @param name: basic file name
    @type name: string

    @return: the pathname to a file in the 'AXE_CONFIG_PATH'-directory
    @rtype: string
    """
    if name == None:
        tmp = os.path.join(AXE_CONFIG_PATH,'/')
    else:
        tmp = os.path.join(AXE_CONFIG_PATH,name)
    return tmp

def putIMAGE(name=None):
    """
    Sets the path to a file in the $AXE_IMAGE_PATH directory

    Appends the input parameter behind the content of the
    (gloal) variable 'AXE_IMAGE_PATH'. Checks for
    multiple directory indicators ('/') before returning
    the result

    @param name: basic file name
    @type name: string

    @return: the pathname to a file in the 'AXE_IMAGE_PATH'-directory
    @rtype: string
    """
    if name == None:
        tmp = os.path.join(AXE_IMAGE_PATH,'/')
    else:
        tmp = os.path.join(AXE_IMAGE_PATH,name)
    return tmp

def putOUTPUT(name=None):
    """
    Sets the path to a file in the $AXE_OUTPUT_PATH directory

    Appends the input parameter behind the content of the
    (gloal) variable 'AXE_OUTPUT_PATH'. Checks for
    multiple directory indicators ('/') before returning
    the result

    @param name: basic file name
    @type name: string

    @return: the pathname to a file in the 'AXE_OUTPUT_PATH'-directory
    @rtype: string
    """
    if name == None:
        tmp = os.path.join(AXE_OUTPUT_PATH,'/')
    else:
        tmp = os.path.join(AXE_OUTPUT_PATH,name)
    return tmp

def putSIMDATA(name=None):
    """
    Sets the path to a file in the $AXE_SIMDATA_PATH directory

    Appends the input parameter behind the content of the
    (gloal) variable 'AXE_SIMDATA_PATH'. Checks for
    multiple directory indicators ('/') before returning
    the result

    @param name: basic file name
    @type name: string

    @return: the pathname to a file in the 'AXE_SIMDATA_PATH'-directory
    @rtype: string
    """
    if name == None:
        tmp = os.path.join(AXE_SIMDATA_PATH,'/')
    else:
        tmp = os.path.join(AXE_SIMDATA_PATH,name)
    return tmp

def putOUTSIM(name=None):
    """
    Sets the path to a file in the $AXE_OUTSIM_PATH directory

    Appends the input parameter behind the content of the
    (gloal) variable 'AXE_OUTSIM_PATH'. Checks for
    multiple directory indicators ('/') before returning
    the result

    @param name: basic file name
    @type name: string

    @return: the pathname to a file in the 'AXE_OUTSIM_PATH'-directory
    @rtype: string
    """
    if name == None:
        tmp = os.path.join(AXE_OUTSIM_PATH,'/')
    else:
        tmp = os.path.join(AXE_OUTSIM_PATH,name)
    return tmp

def putAXESIMBIN(name=None):
    """
    Sets the path to a file in the $AXE_SIMBIN_PATH directory

    Appends the input parameter behind the content of the
    (gloal) variable 'AXE_SIMBIN_PATH'. Checks for
    multiple directory indicators ('/') before returning
    the result

    @param name: basic file name
    @type name: string

    @return: the pathname to a file in the 'AXE_SIMBIN_PATH'-directory
    @rtype: string
    """
    if name == None:
        tmp = os.path.join(AXESIMBIN,'/')
    else:
        tmp = os.path.join(AXESIMBIN, name)
    return tmp

def get_random_filename(dirname=None, ext=None):
    """
    Create a random file name

    The function creates a random filename with a given extension
    and a given path- or general prefix. The random filename
    puts the letters 'tmp' and a five digit, random number between
    the prefix and the extension. It is verified that a random
    filename with an identical filename does NOT exits.

    @param dirname: path- or file- prefix for random filename
    @type dirname: string
    @param ext: the extension of the tmp-file
    @type ext: string

    @return: a random filename of a non-existing file
    @rtype: string
    """
    import random

    # assure a first go in the while loop
    found = 1

    # do until you find a unique name
    while found:

        # get a random int number
        str_num = str(random.randint(10000, 99999))

        # compose a random name
        fname = dirname + 'tmp' + str_num + ext

        # check whether the file exists
        if not os.path.isfile(fname):
            found = 0

    # return the random name
    return fname
