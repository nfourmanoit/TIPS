"""
@author: Martin Kuemmel
@organization: LMU / USM
@license: Gnu Public Licence
@contact: mkuemmel@usm.lmu.de
@version:    $Revision: $
@date:       $Date: $
@changeDate: $LastChangedDate: $
"""
'''
/**
 *
 * Function: get_flambda_from_magab
 * The subroutine calculates the flambda value for a
 * mag_AB value given with its wvavelength as input
 * parameters.
 *
 * Parameters:
 * @param  mag     - the mag_AB value
 * @param  lambda  - the wavelength for mag_AB [nm]
 *
 * Returns:
 * @return flambda - the calculated flambda value
 */
double
get_flambda_from_magab(double mag, double lambda)
{
  double flambda=0.0;
  double fnu=0.0;

  fnu     = pow(10.0, -0.4*(mag+48.6));
  flambda = 1.0e+16*LIGHTVEL*fnu/(lambda*lambda);

  return flambda;
}
'''
def get_flambda_from_magab(mag, wave):
    """
    Computes the F_lambda value for a given MAG_AB at a wavelength
    
    Direct translation of the above C-code. Important: the unit of the
    wavlength is [nm]! 
    """
    fnu = 10**(-0.4*(mag+48.6))
    flambda = 1.0e+16*2.99792458 *fnu/(wave*wave);
    return flambda

def gauss_function(x, a, x0, sigma):
    import numpy
    return a*numpy.exp(-(x-x0)**2/(2*sigma**2))

def doGaussFit(allWavs, oneSpectrum, cog):
    import numpy
    from scipy.optimize import curve_fit

    npWavs = numpy.array(allWavs)
  
    popt, pcov = curve_fit(gauss_function, npWavs, oneSpectrum, p0 = [1., cog, 10.])
    return popt, pcov

def getConstSensitivity(sensitivity):
    """
    Determines the value from a constant sensitivity file
    """
    import pyfits
    
    # open the table and get the
    # central row value
    table = pyfits.open(sensitivity, 'readonly')
    tabData = table[1].data
    midRow = int(float(len(tabData)) / 2.0)
    sensitivity = tabData[midRow][1]
    table.close()

    # return the central value
    return sensitivity

def getFlatSpectrumValue(inSpc, index):
    """
    Determines the value from a constant sensitivity file
    """
    import pyfits
    
    # open the table and get the
    # central row value
    table = pyfits.open(inSpc, 'readonly')
    tabData = table[index].data
    midRow = int(float(len(tabData)) / 2.0)
    flux = tabData[midRow][1]
    table.close()

    # return the central value
    return flux

def getGaussianValues(inSpc, index):
    """
    Determines the value from a constant sensitivity file
    """
    import pyfits
    
    gValues = {}

    # open the table
    table = pyfits.open(inSpc, 'readonly')
    
    tabHeader = table[index].header
    
    # extract the Gaussian parameters
    if 'WAV_LIN' in tabHeader:
        gValues['center'] = tabHeader['WAV_LIN']
    else:
        gValues['center'] = 0.0
    if 'FWHM_LIN' in tabHeader:
        gValues['fwhm'] = tabHeader['FWHM_LIN']
    else:
        gValues['fwhm'] = 0.0
    if 'AMP_LIN' in tabHeader:
        gValues['amp'] = tabHeader['AMP_LIN']
    else:
        gValues['amp'] = 0.0
    
    # close the table
    table.close()

    # return the Gaussian parameters
    return gValues

def getPSFDimension(inPSF):
    import pyfits

    # get the SPF dimension
    psf = pyfits.open(inPSF, 'readonly')    
    dims = psf[1].shape
    psf.close()

    # return the dimension
    return dims

def getModelDimensions(inModel, modelIndex):
    import pyfits

    # get the SPF dimension
    inMod = pyfits.open(inModel, 'readonly')    
    dims = inMod[modelIndex].shape
    inMod.close()

    # return the dimension
    return dims

def extractObjects(inObj, inImage, inModel=None, psfDim=None, simCounts=None):
    import pyfits
    import numpy
    
    # scales the extraction box
    extFactor = 5.0
    
    # beam boundaries w.r.t. 
    # object position
    # could be taken from the configuration file
    xBounds = (15,185)
    
    # open the image
    img = pyfits.open(inImage, 'readonly')

    # go over all objects
    charVals = []
    for index in range(inObj.nrows):
        # open a dictionary
        charQuants = {}

        # get position and size
        xPos = inObj['X_IMAGE'][index]
        yPos = inObj['Y_IMAGE'][index]
        
        if inModel == None:
            # Gaussian object have the object size
            # in the table
            aSize = inObj['A_IMAGE'][index]
            bSize = inObj['B_IMAGE'][index]

            # compute the extraction size
            extSize = aSize*extFactor
            
        else:
            # get the dimension of the model image
            modelIndex = inObj['MODIMAGE'][index]            
            modDims = getModelDimensions(inModel, modelIndex)

            # compute the extraction size
            # from the model image and the PSF size;
            # note that index 0 is in y
            if psfDim == None:
                extSize = int((float(modDims[0])+1.0)/2.0)
            else:
                extSize = int((float(modDims[0])+1.0+float(psfDim[0])+1.0)/2.0)
            #print 'Size: ', extSize, 
 
        # get the beam boundaries
        yUpper = int(yPos+extSize+.5)
        yLower = int(yPos-extSize+.5)
        xUpper = int(xPos+xBounds[1]+.5)
        xLower = int(xPos+xBounds[0]+.5)

        # make the cutout and extract by summing over the 
        # dispersion direction
        cutOut = img[1].data[yLower: yUpper, xLower: xUpper]
        spectrum = numpy.sum(cutOut, 0)
        
        #name = 'outspec%03i.fits' % index
        #pyfits.writeto(name, spectrum)
        
        # get some statistics on the spectrum
        charQuants['ave'] = numpy.average(spectrum)
        charQuants['med'] = numpy.median(spectrum)
        charQuants['std'] = numpy.std(spectrum)

        # if possible, compute the maximum deviation
        if simCounts != None:
            expectCounts = simCounts[index]
            charQuants['maxdev'] = max(numpy.fabs((spectrum-expectCounts)))
            charQuants['maxindex'] = numpy.argmax(numpy.fabs((spectrum-expectCounts)))
            #print '>', charQuants['maxdev'], min(spectrum-expectCounts), max(spectrum-expectCounts), charQuants['maxdev']/expectCounts
        charVals.append(charQuants)

        #print 'median: ', spectrum.shape, numpy.median(spectrum), ' average: ', numpy.average(spectrum),  ' std: ', numpy.std(spectrum)
        #print 'average/std: ', numpy.std(spectrum)/numpy.average(spectrum)

        # get a characteristic e/s value for that dispersion
        #theIndex = int(float(len(spectrum))/2.0)
        #theIndex = 22
        #print theIndex
        #charVals.append(spectrum[int(float(len(spectrum))*3.0/4.0)])
        #charVals.append(spectrum[theIndex])
        #charVals.append(numpy.average(spectrum))
        #print charVals[-1]
        #print spectrum
        #print spectrum.shape
    
    # close the image
    img.close()

    # get back the e/s values
    return charVals

def extractObjectsII(inObj, inImage, inModel=None, psfDim=None):
    import pyfits
    import numpy
    
    # scales the extraction box
    extFactor = 5.0
    
    # beam boundaries w.r.t. 
    # object position
    # could be taken from the configuration file
    xBounds = (15,185)
    
    # open the image
    img = pyfits.open(inImage, 'readonly')

    # go over all objects
    allSpectra = []
    for index in range(inObj.nrows):
        # open a dictionary
        charQuants = {}

        # get position and size
        xPos = inObj['X_IMAGE'][index]
        yPos = inObj['Y_IMAGE'][index]
        
        if inModel == None:
            # Gaussian object have the object size
            # in the table
            aSize = inObj['A_IMAGE'][index]
            bSize = inObj['B_IMAGE'][index]

            # compute the extraction size
            extSize = aSize*extFactor
            
        else:
            # get the dimension of the model image
            modelIndex = inObj['MODIMAGE'][index]            
            modDims = getModelDimensions(inModel, modelIndex)

            # compute the extraction size
            # from the model image and the PSF size;
            # note that index 0 is in y
            if psfDim == None:
                extSize = int((float(modDims[0])+1.0)/2.0)
            else:
                extSize = int((float(modDims[0])+1.0+float(psfDim[0])+1.0)/2.0)
            #print 'Size: ', extSize, 
 
        # get the beam boundaries
        yUpper = int(yPos+extSize+.5)
        yLower = int(yPos-extSize+.5)
        xUpper = int(xPos+xBounds[1]+.5)
        xLower = int(xPos+xBounds[0]+.5)

        # make the cutout and extract by summing over the 
        # dispersion direction
        cutOut = img[1].data[yLower: yUpper, xLower: xUpper]
        spectrum = numpy.sum(cutOut, 0)

        # append the spectrum
        allSpectra.append(spectrum)
    
    # close the image
    img.close()

    # get back the e/s values
    return allSpectra

def verify(inImage, inCat, inConf, inSpec=None, inModel=None, inPSF=None):
    import os.path
    import axesim
    from axesim import modspeclist

    # analyze the config file to get some input,
    # e.g. the sensitivity file name, the dispersion
    # the beam size.
    # emulated here
    sensFile = os.path.join(os.environ['AXE_CONFIG_PATH'], 'constSensI.fits')
    sensitivity = getConstSensitivity(sensFile)
    
    # if possible, get the PSF dimensions
    if inPSF != None:
        # get the PSF dimensions
        psfDim = getPSFDimension(inPSF)
    else:
        psfDim = None


    # load the object list
    inObj = modspeclist.MagColList(inCat)

    # check whether there are spectra
    magColIndex = None
    wavelength  = None
    mSpecCol    = None
    mImgCol     = None
    if inSpec == None:
        # confirm there is only one magnitude column
        if len(inObj.mag_cols) != 1:
            errMsg = 'There should be only one magnitude column in: %s' % inCat
            raise Exception(errMsg)
        magColIndex = inObj.mag_cols[0][0]
        wavelength  = inObj.mag_cols[0][1]
    else:
        # confirm and store the model spectrum column
        if inObj.find('MODSPEC') < 1:
            errMsg  = 'Missing column MODSPEC in table %s!' % inCat
            raise Exception(errMsg)
        mSpecCol = inObj.find('MODSPEC')

    # confirm and store the model image column
    if inModel != None:
        if inObj.find('MODIMAGE') < 1:
            errMsg  = 'Missing column MODIMAGE in table %s!' % inCat
            raise Exception(errMsg)
        mImgCol = inObj.find('MODIMAGE')

    simCounts = []
    simFlux   = []
    for index in range(inObj.nrows):
        
        if mSpecCol != None:
            # get the model spectrum value
            mSpc = inObj[mSpecCol][index]
            fluxVal = getFlatSpectrumValue(inSpec, mSpc)
        else:          
            # convert the AB-mag value to flux then to counts
            magVal = inObj[magColIndex][index]
            fluxVal = get_flambda_from_magab(magVal, wavelength)
        
        # compute the expected count value
        countVal = fluxVal*sensitivity*50.0
        
        # append the counts to the list
        simCounts.append(countVal)

        # append the flux to the list
        simFlux.append(fluxVal)

    # 'extract' the spectra and get one characteristic e/s value
    # for each object
    charVals = extractObjects(inObj, inImage, inModel=inModel, psfDim=psfDim, simCounts=simCounts)

    # go over all objects
    toFlux = 1.0/sensitivity/50.0
    for index in range(inObj.nrows):
        
        # get the flux from the extracted value
        #charFlux  = charVals[index]['ave']/sensitivity/50.0
        charFlux  = charVals[index]['ave']*toFlux
        charVals[index]['ave']    = charVals[index]['ave']*toFlux
        charVals[index]['med']    = charVals[index]['med']*toFlux
        charVals[index]['maxdev'] = charVals[index]['maxdev']*toFlux
        charVals[index]['std']    = charVals[index]['std']*toFlux

    # return the simulated
    # and extracted flux values
    return simFlux, charVals

def verifyII(inImage, inCat, inConf, inSpec=None, inModel=None, inPSF=None):
    import os.path
    import axesim
    from axesim import modspeclist

    # analyze the config file to get some input,
    # e.g. the sensitivity file name, the dispersion
    # the beam size.
    # emulated here
    sensFile = os.path.join(os.environ['AXE_CONFIG_PATH'], 'constSensI.fits')
    sensitivity = getConstSensitivity(sensFile)
    
    # if possible, get the PSF dimensions
    if inPSF != None:
        # get the PSF dimensions
        psfDim = getPSFDimension(inPSF)
    else:
        psfDim = None


    # load the object list
    inObj = modspeclist.MagColList(inCat)

    # check whether there are spectra
    magColIndex = None
    wavelength  = None
    mSpecCol    = None
    mImgCol     = None
    if inSpec == None:
        # confirm there is only one magnitude column
        if len(inObj.mag_cols) != 1:
            errMsg = 'There should be only one magnitude column in: %s' % inCat
            raise Exception(errMsg)
        magColIndex = inObj.mag_cols[0][0]
        wavelength  = inObj.mag_cols[0][1]
    else:
        # confirm and store the model spectrum column
        if inObj.find('MODSPEC') < 1:
            errMsg  = 'Missing column MODSPEC in table %s!' % inCat
            raise Exception(errMsg)
        mSpecCol = inObj.find('MODSPEC')

    # confirm and store the model image column
    if inModel != None:
        if inObj.find('MODIMAGE') < 1:
            errMsg  = 'Missing column MODIMAGE in table %s!' % inCat
            raise Exception(errMsg)
        mImgCol = inObj.find('MODIMAGE')

    simVals= []
    for index in range(inObj.nrows):
        
        if mSpecCol != None:
            # get the model spectrum value
            simVals.append(getGaussianValues(inSpec, inObj[mSpecCol][index]))
        else:          
            simVals.append(None)

    # 'extract' the spectra and get one characteristic e/s value
    # for each object
    allSpectra = extractObjectsII(inObj, inImage, inModel=inModel, psfDim=psfDim)

    # go over all objects
    cogVals = []
    fitVals = []
    for oneSpectrum in allSpectra:
        index=0
        weight=0.0
        sum=0.0
        allWavs = []
        for oneVal in oneSpectrum:
            actWav = 1.0E+03+5.0*(float(index)+15.+1)
            sum += actWav*oneVal
            weight+=oneVal
            index+=1
            allWavs.append(actWav)
        cogVals.append(sum/weight)

        popt, pcov = doGaussFit(allWavs, oneSpectrum, sum/weight)
        fitVals.append(popt)

    # return the simulated
    # and extracted flux values
    return simVals, fitVals, cogVals

def getInitialModIndex(tipscat, axesimcat):
    import pyfits
    import axesim
    from axesim import modspeclist
    import numpy
    
    tipsObj = pyfits.open(tipscat)
    tipsId = numpy.asarray(tipsObj[1].data.field("NUMBER"))
    
    axesimObj = modspeclist.MagColList(axesimcat)
    axesimId = axesimObj['ID'].tonumpy()
    
    try:
        tipsModSpc = numpy.asarray(tipsObj[1].data.field("MODSPEC"))        
        for i in range(axesimObj.nrows):
            s = (tipsId==axesimId[i])
            if len(s.nonzero()[0])>0:
                index=s.nonzero()[0][0]
                axesimObj['MODSPEC'][i] = int(tipsModSpc[index])
    except KeyError:
        pass
    
    try:
        tipsModImg = numpy.asarray(tipsObj[1].data.field("MODIMG"))        
        for i in range(axesimObj.nrows):
            s = (tipsId==axesimId[i])
            if len(s.nonzero()[0])>0:
                index=s.nonzero()[0][0]
                axesimObj['MODIMAGE'][i] = int(tipsModImg[index])
    except KeyError:
        pass
    
    axesimObj.flush()
