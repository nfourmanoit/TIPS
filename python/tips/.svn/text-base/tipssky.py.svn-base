"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

TIPS classes to manage sky objects.
"""

import os
import os.path
import asciidata
import pyfits
import numpy
import shutil

from tipserror import *

class SkySources:
        """
        Class to store the sky source model
        """

        def __init__(self, inCatDir, inSpcDir=None, inCatForm='TIPS', inSpcForm='TIPS', inThmDir=None, inThmForm='TIPS', silent=True):
                """
                Constructor: Initializes the class
                
                @param inCatDir: input catalog directory (fits or ascii with a sextractor header)
                @type inCatDir: string
                @param inSpcDir: input (fits) spectra directory
                @type inSpcDir: string
                @param inCatForm: input catalog format (TIPS or CMC, see doc for more details)
                @type inCatForm: string
-               @param inSpcForm: input spectra format (CMC = TIPS, aXeSIM, SplitFits or SplitAscii, see doc for more details)
                @type inSpcForm: string
                """

                self.inCatDir = inCatDir
                self.inSpcDir = inSpcDir
                self.inCat = None
                self.inCatType = None
                self.inCatForm = inCatForm
                self.nSources = 0
                self.inSpc = None
                self.inSpcForm = inSpcForm
                self.inSpcType = None
                self.inColDict = None
                self.colDict = ["NUMBER", "RA", "DEC", "A_SKY", "B_SKY", "THETA_SKY", "MODSPEC", "MODFILE", "MODIMG", "IMGFILE"]
                self.inThmDir = inThmDir
                self.inThm = None
                self.inThmForm = inThmForm
                self.inThmType = 'fits'
                self.silent = silent
                
                self.checkInput()

        def loadCat(self):
                """
                Method to load an input sources catalog.
                """

                try:
                        self.inCat = pyfits.open(self.inCatDir)
                        self.inCatType = 'fits'
                        self.nSources = self.inCat[1].data.shape[0]
                except IOError:
                        try:
                                self.inCat = asciidata.open(self.inCatDir)
                                self.inCatType = 'ascii'
                                self.nSources = len(self.inCat[0])
                        except:
                                error_message = 'Can not load input sources catalog file:' + self.inCatDir
                                raise TIPSError(error_message)

        def checkInput(self):
                """
                Method to check inputs
                """
                
                if self.inCatDir != None:
                    if not os.path.isfile(self.inCatDir):
                        error_message = 'The input sources catalog does not exist:' + self.inCatDir
                        raise TIPSError(error_message)

                    if self.inCatForm == 'CMC':
                        self.loadCat()
                        self.inColDict = ["Id", "RA", "DEC", "A_IMAGE", "B_IMAGE", "THETA_IMAGE", "SpcExt", "MODFILE", "MODIMG", "IMGFILE"]

                    elif self.inCatForm == 'TIPS':
                        self.loadCat()
                        self.inColDict = ["NUMBER", "RA", "DEC", "A_SKY", "B_SKY", "THETA_SKY", "MODSPEC", "MODFILE", "MODIMG", "IMGFILE"]

                    else:
                        error_message = 'The input format parameter inCatForm is unknown:'+self.inCatForm
                        raise TIPSError(error_message)

                    if self.inSpcForm=='CMC' or self.inSpcForm=='TIPS' or  self.inSpcForm=='aXeSIM':
                        if self.inSpcDir!= None and not os.path.isfile(self.inSpcDir):
                                error_message = 'The input spectra file does not exist:' + self.inSpcDir
                                raise TIPSError(error_message)
                        self.inSpcType = 'fits'
                        
                    elif self.inSpcForm=='SplitFits':
                        self.inSpcType = 'fits'
                        self.inSpcForm='Split'
                
                    elif self.inSpcForm=='SplitAscii':
                        self.inSpcType = 'ascii'
                        self.inSpcForm='Split'
                
                    else:
                        error_message = 'The input format parameter inSPCForm is unknown:'+self.inSpcForm
                        raise TIPSError(error_message)

                    if self.inThmForm=='TIPS' or  self.inThmForm=='aXeSIM':
                        if self.inThmDir!=None and not os.path.isfile(self.inThmDir):
                                error_message = 'The input thumbnail file does not exist:' + self.inThmDir
                                raise TIPSError(error_message)
                        self.inThmType = 'fits'
                        
                    elif self.inThmForm=='SplitFits':
                        self.inThmType = 'fits'
                        self.inThmForm='Split'
                
                    else:
                        error_message = 'The input format parameter inThmForm is unknown:'+self.inThmForm
                        raise TIPSError(error_message)
                else:
                    if not self.silent:
                        warning_message = 'The input catalog is not defined, simulation of a dark'
                        print TIPSWarning(warning_message)
                    if self.inSpcDir != None or self.inThmDir != None:
                        error_message = 'The input catalog is not defined but the spectrum or thumbnail catalog is defined'
                        raise TIPSError(error_message)

        def getCatCol(self, colId):
                """
                Method to get a column from the input catalog 

                @param colId: column name
                @type colId: string
                
                @return: the column named colId
                @rtype: numpy array
                """

                try:
                        iCol = self.colDict.index(colId)
                except ValueError:
                        error_message = 'Can not get column in dictionnary:' + colId
                        raise TIPSError(error_message)

                jCol = self.inColDict[iCol]
                
                if self.inCatType == 'ascii':
                        kCol = self.inCat.find(jCol)
                        if kCol < 0:
                                error_message = 'Can not find the column in CMC catalog (ascii):'+jCol
                                raise TIPSError(error_message)
                        col = self.inCat[jCol].tonumpy()
                elif self.inCatType == 'fits':
                        try:
                                col = self.inCat[1].data.field(jCol)
                        except KeyError:
                                error_message = 'Can not find the column in CMC catalog (fits):'+jCol
                                raise TIPSError(error_message)

                # in the CMC A_IMAGE and B_IMAGE are in pixels with 1 pixel = 0.03 arcsec
                # convert A_IMAGE and B_IMAGE in arcsec
                if self.inCatForm == 'CMC' and (jCol == "A_IMAGE" or jCol == "B_IMAGE"):
                        col *= 0.03
                
                return col

        def loadSpcFile(self, index=0):
                """
                Method to load an input spectra catalog.
                """
                if self.inSpcForm == 'Split':
                        filePath = self.getCatCol("MODFILE")[index]
                else:
                        filePath = self.inSpcDir
                if filePath != self.inSpcDir or self.inSpc==None:
                        self.closeSpc()
                        if self.inSpcType == 'fits':
                                self.inSpc = pyfits.open(filePath, memmap=False)
                        elif self.inSpcType == 'ascii':
                                self.inSpc = numpy.transpose(numpy.loadtxt(filePath))
                self.inSpcDir=filePath

        def closeSpc(self):
                """
                Method to close the input spectra catalog.
                (Usefull to avoid memory leak)
                """

                if self.inSpc != None and self.inSpcType == 'fits':
                        self.inSpc.close()
                del self.inSpc
                self.inSpc = None

        def getSpc(self, hdu=0):
                """
                Method to get a spectrum from a spectra file
                
                @param hdu: hdu of the object, necessary only for fits files
                @type hdu: integer
                
                @return: the spectra stored in the hdu spcExt (wave in A, flux in erg/s/cm2/A)
                @rtype: numpy array tuple ([float],[float])
                """

                if self.inSpcType == 'ascii':
                        wave = self.inSpc[0]
                        flux = self.inSpc[1]
                elif self.inSpcForm == 'aXeSIM':
                        wave = numpy.asarray(self.inSpc[hdu].data.field('WAV_NM'))*10.0
                        flux = numpy.asarray(self.inSpc[hdu].data.field('FLUX'))          
                else:
                        wave = numpy.asarray(self.inSpc[hdu].data.field('lambda'))
                        flux = numpy.asarray(self.inSpc[hdu].data.field('flux'))

                return (wave,flux)

        def getSpcIndex(self, index):
                """
                Method to get a spectrum from the object index.
                
                @param index: index of the object
                @type index: integer
                
                @return: the spectra stored in the hdu spcExt (wave in A, flux in erg/s/cm2/A)
                @rtype: numpy array tuple ([float],[float])
                """
        
                self.loadSpcFile(index)
                if self.inSpcType == 'fits':
                        spcExt = self.getCatCol("MODSPEC")[index]
                else:
                        spcExt = 0
                return self.getSpc(spcExt)

        def getSpcIdent(self, ident):
                """
                Method to get a spectrum from the object id number.
                
                @param ident: identifier of the object
                @type ident: integer
                
                @return: the spectra stored in the hdu spcExt (wave in A, flux in erg/s/cm2/A)
                @rtype: numpy array tuple ([float],[float])
                """

                ids = self.getCatCol("NUMBER")
                s = (ids==ident)
                if len(s.nonzero()[0])>0:
                        index=s.nonzero()[0][0]
                        return self.getSpcIndex(index)
                else:
                        error_message = 'Object ID %d could not be found' % (ident)
                        raise TIPSError(error_message)
 
        def loadThmFile(self, index=0):
                """
                Method to load an input thumbnail catalog.
                """
                if self.inThmForm == 'Split':
                        filePath = self.getCatCol("IMGFILE")[index]
                else:
                        filePath = self.inThmDir
                
                if filePath != self.inThmDir or self.inThm==None:
                        self.closeThm()
                        self.inThm = pyfits.open(filePath, memmap=False)
                self.inThmDir=filePath

        def closeThm(self):
                """
                Method to close the input thumbnail catalog.
                (Usefull to avoid memory leak)
                """

                if self.inThm != None:
                        self.inThm.close()
                del self.inThm
                self.inThm = None

        def getThm(self, hdu=0, pixscl=None):
                """
                Method to get a thumbnail from a spectra file
                
                @param hdu: hdu of the object, necessary only for fits files
                @type hdu: integer
                
                @return: the thumbnail stored in the hdu modimg and the scale factor
                @rtype: numpy array tuple ([float],float)
                """

                img = numpy.asarray(self.inThm[hdu].data)
                try:
                    smpfac = float(self.inThm[hdu].header['SMPFAC'])
                    if smpfac <= 0.0:
                        error_message = 'Sampling factor must be positive: %f' % smpfac
                        raise TIPSError(error_message)
                except KeyError, ValueError:
                    smpfac = None                 
                
                if smpfac==None and pixscl!=None:
                    try:
                        sclimg = float(self.inThm[hdu].header['PIXSCL'])
                        smpfac = pixscl / sclimg
                    except KeyError, ValueError:
                        smpfac = None
                return (img,smpfac)

        def getThmIndex(self, index, pixscl=None):
                """
                Method to get a thumbnail from the object index.
                
                @param index: index of the object
                @type index: integer
                
                @return: the thumbnail stored in the hdu modimg and the scale factor
                @rtype: numpy array tuple ([float],float)
                """
        
                thmExt = self.getCatCol("MODIMG")[index]
                if thmExt < 0:
                    img = numpy.zeros((51,51))
                    img[25,25] = 1
                    return(img, None)
                else:
                    self.loadThmFile(index)
                    return self.getThm(thmExt, pixscl)

        def getThmIdent(self, ident, pixscl=None):
                """
                Method to get a thumbnail from the object id number.
                
                @param ident: identifier of the object
                @type ident: integer
                
                @return: the thumbnail stored in the hdu modimg and the scale factor
                @rtype: numpy array tuple ([float],float)
                """

                ids = self.getCatCol("NUMBER")
                s = (ids==ident)
                if len(s.nonzero()[0])>0:
                        index=s.nonzero()[0][0]
                        return self.getThmIndex(index, pixscl)
                else:
                        error_message = 'Object ID %d could not be found' % (ident)
                        raise TIPSError(error_message)

        def reset(self, newCatDir=None, newSpcDir=None, newCatForm=None, newSpcForm=None, newThmDir=None, newThmForm=None):
                """
                Method to reset input sources catalog.

                @param newCatDir: input catalog directory (fits or ascii with a sextractor header)
                @type newCatDir: string
                @param newSpcDir: input (fits) spectra directory
                @type newSpcDir: string
                @param newCatForm: input catalog format (for now only CMC is implemented)
                @type newCatForm: string
-               @param newSpcForm: input spectra format (for now only CMC and aXeSIM formats are implemented)
                @type newSpcForm: string
                """

                if newCatDir!=None:
                        if newCatForm != None:
                                self.inCatForm = newCatForm
                        else:
                                if not self.silent:
                                    warning_message = 'Catalog format have not be reset.'
                                    print TIPSWarning(warning_message)

                        self.inCatDir = newCatDir

                        if self.inCat != None:
                                if self.inCatType == 'fits':
                                        self.inCat.close()
                                self.inCat = None
                                self.inCatType = None
                                self.nSources = 0

                        if newSpcDir==None:
                                if not self.silent:
                                    warning_message = 'Catalog have been reset without update spectra.'
                                    print TIPSWarning(warning_message)
                        
                if newSpcDir!=None:
                        if newSpcForm != None:
                                self.inSpcForm = newSpcForm
                        else:
                                if not self.silent:
                                    warning_message = 'Spectra format have not be reset.'
                                    print TIPSWarning(warning_message)

                        self.inSpcDir = newSpcDir

                        if self.inSpc != None:
                                self.inSpc.close()
                                self.inSpc = None

                        if newCatDir==None:
                                if not self.silent:
                                    warning_message = 'Spectra have been reset without update catalog sources.'
                                    print TIPSWarning(warning_message)
                                
                if newThmDir!=None:
                        if newThmForm != None:
                                self.inThmForm = newThmForm
                        else:
                                if not self.silent:
                                    warning_message = 'Thumbnail format have not be reset.'
                                    print TIPSWarning(warning_message)

                        self.inThmDir = newThmDir

                        if self.inThm != None:
                                self.inThm.close()
                                self.inThm = None

                        if newCatDir==None:
                                if not self.silent:
                                    warning_message = 'Thumbnail have been reset without update catalog sources.'
                                    print TIPSWarning(warning_message)
        
                if newCatForm!=None and newCatDir==None:
                        self.inCatForm = newCatForm
                        if not self.silent:
                            warning_message = 'Catalog format have been without reset the catalog.'
                            print TIPSWarning(warning_message)

                if newSpcForm!=None and newSpcDir==None:
                        self.inSpcForm = newSpcForm
                        if not self.silent:
                            warning_message = 'Spectra format have been without reset the catalog.'
                            print TIPSWarning(warning_message)
                        
                if newThmForm!=None and newThmDir==None:
                        self.inSpcForm = newThmForm
                        if not self.silent:
                            warning_message = 'Thumbnail format have been without reset the catalog.'
                            print TIPSWarning(warning_message)
                        
                self.checkInput()
                
        def close(self):
                self.closeSpc()
                self.closeThm()
                del self.inCatDir
                del self.inSpcDir
                del self.inThmDir
                if self.inCatType == 'fits' and self.inCat != None:
                        self.inCat.close()
                del self.inCat
                del self.inCatType
                del self.inCatForm
                del self.nSources
                del self.inThm
                del self.inSpc
                del self.inThmForm
                del self.inSpcForm 
                del self.inSpcType
                del self.inThmType
                del self.colDict
                del self

class SkyNoise:
        """
        Class to store the sky noise model
        """

        def __init__(self,lambda_min=None, lambda_max=None, lambda_step=None):
                """
                Constructor: Initializes the class
                
                @param lambda_min: minimum wavelenght in A of the noise spectrum (you can set it later)
                @type lambda_min: float
                @param lambda_max: maximum wavelenght in A of the noise spectrum (you can set it later)
                @type lambda_max: float
                @param lambda_step: wavelenght step in A of the noise spectrum (you can set it later)
                @type lambda_step: float
                """
                
                if lambda_min!=None and lambda_max!=None and lambda_step!=None:
                        self.wave = numpy.arange(start=lambda_min, stop=lambda_max, step=lambda_step, dtype=float)
                        self.flux = numpy.zeros(len(self.wave))
                else:
                        self.wave = None
                        self.flux = None

        def getFluxFromAldering02(self, wave, scale=1.0):
                """
                Method to set noise spectrum with a zodical model of Aldering et al. 2002.
                
                @param wave: wavelength array
                @type wave: numpy [float]
                @param scale: scale factor
                @type scale: float

                @return: flux in erg/s/cm2/arcsec2/A
                @rtype: numpy array [float]
                """
                
                flux = numpy.zeros(len(wave))
                flux[(wave>4000.0)&(wave<=6100.0)] = 10**(-17.755)
                flux[(wave>6100.0)&(wave<22000.0)] = 10**(-17.755 - 0.730*((wave[(wave>6100.0)&(wave<22000.0)]/10000.0)-0.61))

                return flux*scale

        def getSpcFromFile(self, spcDir):
                """
                Method to set noise spectrum from file.
                
                @param spcDir: Directory of the spectrum file.
                If ascii format the two first columns have to be wavelenght in A and flux in erg/s/cm2/arcsec2/A
                If fits format the table have to be in hdu 1 and the wavelenght have to be in the "lambda" field and the flux in the "flux" field.
                @type spcDir: string

                @return: spectra (wave in A, flux in erg/s/cm2/arcsec2/A)
                @rtype: numpy array tuple ([float],[float])
                """

                try:
                        spcFits = pyfits.open(spcDir)
                        wave = numpy.asarray(spcFits[1].data.field('lambda'))
                        flux = numpy.asarray(spcFits[1].data.field('flux'))
                except IOError:
                        try:
                                spc = numpy.loadtxt(spcDir, unpack=True)
                                wave = spc[0]
                                flux = spc[1]
                        except:
                                error_message = 'Can not load input noise spectrum from file:' + spcDir
                                raise TIPSError(error_message)
                except ValueError:
                        error_message = 'Can not load field "lambda" and/or "flux" from fits input:' + spcDir

                return (wave, flux)

        def addContanteNoise(self, noiseValue, lambda_min=None, lambda_max=None, lambda_step=None):
                """
                Method to add a constant noise.

                @param noiseValue: noise value in erg/s/cm2/arcsec2/A
                @type noiseValue: float
                @param lambda_min: minimum wavelenght in A of the noise spectrum (useless if already set)
                @type lambda_min: float
                @param lambda_max: maximum wavelenght in A of the noise spectrum (useless if already set)
                @type lambda_max: float
                @param lambda_step: wavelenght step in A of the noise spectrum (useless if already set)
                @type lambda_step: float
                """
                if self.wave == None:
                        if lambda_min!=None and lambda_max!=None and lambda_step!=None:
                                self.wave = numpy.arange(start=lambda_min, stop=lambda_max, step=lambda_step, dtype=float)
                                self.flux = noiseValue*numpy.ones(len(self.wave))
                        else:
                                error_message = 'Wavelength parameters have to be set.'
                                raise TIPSError(error_message)
                else:
                        self.flux += noiseValue
                        if lambda_min!=None or lambda_max!=None or lambda_step!=None:
                                warning_message = 'Wavelength is already set, lambda_min, lambda_max, lambda_step parameters have been ignored'
                                print TIPSWarning(warning_message)

        def addAldering02Noise(self, scale=1.0, lambda_min=None, lambda_max=None, lambda_step=None):
                """
                Method to add zodiacal noise from Aldering et al. 2002 model.

                @param scale: scale apply to the model
                @type scale: float
                @param lambda_min: minimum wavelenght in A of the noise spectrum (useless if already set)
                @type lambda_min: float
                @param lambda_max: maximum wavelenght in A of the noise spectrum (useless if already set)
                @type lambda_max: float
                @param lambda_step: wavelenght step in A of the noise spectrum (useless if already set)
                @type lambda_step: float
                """

                if self.wave == None:
                        if lambda_min!=None and lambda_max!=None and lambda_step!=None:
                                self.wave = numpy.arange(start=lambda_min, stop=lambda_max, step=lambda_step, dtype=float)
                                self.flux = self.getFluxFromAldering02(self.wave, scale)
                        else:
                                error_message = 'Wavelength parameters have to be set.'
                                raise TIPSError(error_message)
                else:
                        self.flux += self.getFluxFromAldering02(self.wave, scale)
                        if lambda_min!=None or lambda_max!=None or lambda_step!=None:
                                warning_message = 'Wavelength is already set, lambda_min, lambda_max, lambda_step parameters have been ignored'
                                print TIPSWarning(warning_message)

        def addSpcNoise(self, spcDir, interp_warn=True):
                """
                Method to add noise from a spectrum file.

                @param spcDir: path to the file containing the spectrum.
                @type spcDir: string
                @param interp_warn: if True, print warning if the spectrum have to be interpolated.
                @type interp_warn: bool 
                """

                if self.wave == None:
                        (self.wave,self.flux) = self.getSpcFromFile(spcDir)
                else:
                        (wave,flux) = self.getSpcFromFile(spcDir)
                        self.flux += numpy.interp(self.wave,wave,flux,left=0.0, right=0.0)
                        if interp_warn:
                                warning_message = 'Wavelength is already set, value in the spectrum file have been interpolated.'
                                print TIPSWarning(warning_message)

        def close(self):
                del self.wave
                del self.flux
                del self


class SkyAbs:
        """
        Class to store the sky absorption model.
        """

        def __init__(self,lambda_min=None, lambda_max=None, lambda_step=None):
                """
                Constructor: Initializes the class

                @param lambda_min: minimum wavelenght in A of the noise spectrum (you can set it later)
                @type lambda_min: float
                @param lambda_max: maximum wavelenght in A of the noise spectrum (you can set it later)
                @type lambda_max: float
                @param lambda_step: wavelenght step in A of the noise spectrum (you can set it later)
                @type lambda_step: float
                """
                
                if lambda_min!=None and lambda_max!=None and lambda_step!=None:
                        self.wave = numpy.arange(start=lambda_min, stop=lambda_max, step=lambda_step, dtype=float)
                        self.trans = numpy.ones(len(self.wave))
                else:
                        self.wave = None
                        self.trans = None
                        self.ext=None
                        self.ebv=None

        def getSpcFromFile(self, spcDir, key='transmission'):
                """
                Method to get sky absortion from a file.
                
                @param spcDir: Directory of the spectrum file.
                If ascii format the two first columns have to be wavelenght in A and transmission or extinction.
                If fits format the table have to be in hdu 1 and the wavelenght have to be in the "lambda" field and the transmission or extinction field name is defined with the parameter key.
                @type spcDir: string
                @param key: name of the transmission or extinction field.
                @type key: string

                @return: spectra (wave in A, transmission or extinction)
                @rtype: numpy array tuple ([float],[float])
                """

                try:
                        spcFits = pyfits.open(spcDir)
                        wave = numpy.asarray(spcFits[1].data.field('lambda'))
                        abs = numpy.asarray(spcFits[1].data.field(key))
                except IOError:
                        try:
                                spc = numpy.loadtxt(spcDir, unpack=True)
                                wave = spc[0]
                                abs= spc[1]
                        except:
                                error_message = 'Can not load input noise spectrum from file:' + spcDir
                                raise TIPSError(error_message)
                except ValueError:
                        error_message = 'Can not load field "lambda" and/or "%s" from fits input: %s'%(key, spcDir)

                return (wave, abs)

        def setFromTrans(self, spcDir, scale=1.0, interp_warn=True):
                """
                Method to set the sky absortion with a spectrum (lambda in A, transmission).

                @param spcDir: path to the file containing the spectrum.
                @type spcDir: string
                @param scale: scale factor
                @type scale: float
                @param interp_warn: if True, print warning if the spectrum have to be interpolated.
                @type interp_warn: bool 
                """
                if self.wave == None:
                        (wave,trans) = self.getSpcFromFile(spcDir, key='transmission')
                        self.wave = wave
                        self.trans = scale*trans
                else:
                        (wave,trans) = self.getSpcFromFile(spcDir)
                        self.trans = scale*numpy.interp(self.wave,wave,trans,left=1.0, right=1.0)
                        if interp_warn:
                                warning_message = 'Wavelength is already set, value in the spectrum file have been interpolated.'
                                print TIPSWarning(warning_message)
                self.ext=None
                self.ebv=None

        def setFromExt(self, spcDir, ebv=1.0, interp_warn=True):
                """
                Method to set the sky absortion with a spectrum (lambda in A, extinction).

                @param spcDir: path to the file containing the spectrum.
                @type spcDir: string
                @param ebv: E(B-V)
                @type ebv: float
                @param interp_warn: if True, print warning if the spectrum have to be interpolated.
                @type interp_warn: bool 
                """

                if self.wave == None:
                        (self.wave,self.ext) = self.getSpcFromFile(spcDir, key='extinction')
                else:
                        (wave,ext) = self.getSpcFromFile(spcDir, key='extinction')
                        self.ext = numpy.interp(self.wave,wave,ext,left=0.0, right=0.0)
                        if interp_warn:
                                warning_message = 'Wavelength is already set, value in the spectrum file have been interpolated.'
                                print TIPSWarning(warning_message)

                self.ebv = ebv
                self.trans = 10**(-0.4*self.ext*self.ebv)

        def resetEBV(self, ebv):
                """
                Method to reset the E(B-V) value and recompute the sky transmission.

                @param ebv: E(B-V)
                @type ebv: float
                """

                if self.ebv == None:
                        error_message = 'Extinction is not set.'
                        print TIPSError(error_message)
                else:
                        self.ebv = ebv
                        self.trans = 10**(-0.4*self.ext*self.ebv)

        def close(self):
                del self.wave
                del self.trans
                del self.ext
                del self.ebv
                del self

