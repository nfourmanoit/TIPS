"""
$Revision: 1.1 $ $Date: 2008/09/05 08:01:40 $
Author: Martin Kuemmel (mkuemmel@stecf.org)
Affiliation: Space Telescope - European Coordinating Facility
WWW: http://www.stecf.org/software/slitless_software/axesim/
"""
class aXeSIMError(Exception):
    """
    General Error in aXeSIM

    This class is just a simple extension to the general exception class.
    All errors in 'axesim' are thrown using this class to be able
    to distinguish them from different errors.
    """
    def __init__(self, message):
        """
        Initializer for the class

        @param message: message associated to the exception
        @type message: string
        """
        self.message = message

    def __str__(self):
        """
        String method for the class

        @return: the string representation of the class
        @rtype: string
        """
        return self.message
