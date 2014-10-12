"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

TIPS classes to manage errors.
"""

class TIPSError(Exception):
    """
    General Error in TIPS
    Source: aXeSIMError
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

class TIPSWarning(Exception):
    """
    General Warning in TIPS
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
        return 'Warning: '+self.message

