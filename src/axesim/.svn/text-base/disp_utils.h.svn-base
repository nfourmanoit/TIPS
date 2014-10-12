/**
 *  File: disp_utils.c
 *  Subroutines to calculate the
 *  various contamination models
 *
 * @author  Martin Kuemmel, Julien Zoubian
 * @package disp_utils
 * @version $Revision: 1.0 $
 * @date    $Date: 2010/05/20 10:35:43 $
 */
#ifndef _DISP_UTILS_H
#define _DISP_UTILS_H

#include <time.h>
#include <math.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_interp.h>
#include "inout_aper.h"
#include "aXe_grism.h"
#include "spce_sect.h"
#include "spc_back.h"
#include "spce_PET.h"
#include "spc_wl_calib.h"
#include "aXe_errors.h"
#include "fringe_conf.h"
#include "spc_resp.h"
#include "spce_pathlength.h"
#include "aper_conf.h"
#include "specmodel_utils.h"
#include "model_utils.h"
#include "spc_fluxcube.h"
#include "spc_model.h"


extern int
compute_disp(char grism_file[], char OAF_file[], char CONF_file[],
	     const char specmod_file[],  const char objmod_file[], const double lambda_psf, observation *obs);

extern int
add2image(const px_point npixels, observation *obs, beamspec *spec);

extern int
add2roij(const dirobject *actdir, const tracedata *acttrace, const d_point dpixel, const spectrum *resp,
		beamspec * actspec, const calib_function  *wl_calibration, fitsfile *ROIJ_fitsptr, char ID[60]);

#endif
