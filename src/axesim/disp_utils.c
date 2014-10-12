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

#include <time.h>
#include <math.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_interp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fitsio.h>
#include <unistd.h>
#include "aXe_utils.h"
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
#include "crossdisp_utils.h"
#include "disp_utils.h"
#include "spc_FITScards.h"

/**
 * Function: compute_disp
 * The function computes the grism image.
 */
int
compute_disp(char grism_file[], char OAF_file[], char CONF_file[],
		const char specmod_file[],  const char objmod_file[], const double lambda_psf, observation *obs)
{
	object **oblist;

	beamspec *spec;

	fits_access *spectrum_access;
	fits_access *modim_access;

	px_point npixels;
	gsl_matrix *drzcoeffs;
	int nobjects=0;
	int i=0;
	int j=0;
	int beamID;
	int max_offs;

	calib_function *wl_calibration;
	double psf_offset=0;
	spectrum *resp;

	aperture_conf *conf;

	beam actbeam;

	int nx, ny;
	d_point dpixel;
	double sval;

	int f_status = 0;

	dirobject *actdir;
	tracedata *acttrace;

	FITScards *gcards;

	char ID[60];

	// load the object list
	fprintf (stdout, "aXe_DISPIMAGE: Loading object aperture list...");
	oblist = file_to_object_list_seq (OAF_file, obs);
	fprintf (stdout,"%d objects loaded.\n",object_list_size(oblist));

	// check whether highres spectra are given are available
	if (strlen(specmod_file) > 0) {
		// load the spectral models
		fprintf (stdout, "aXe_DISPIMAGE: Loading spectral models...");
		spectrum_access = access_fits_models(specmod_file);
		// report the number of models loaded
		fprintf (stdout,"%d models available.\n", spectrum_access->n_modelHDU);
	}
	else {
		// or set the struct to NULL
		spectrum_access = NULL;
	}

	// check whether direct emission models are available
	if (strlen(objmod_file) > 0) {
		// load the image models
		fprintf (stdout, "aXe_DISPIMAGE: Loading direct image models...");
		modim_access = access_fits_models(objmod_file);
		objmod_file = NULL;
		fprintf (stdout,"%d images available.\n", modim_access->n_modelHDU);
	}
	else {
		modim_access = NULL;
	}

	// allocate memory for the error-matrix, which is used for the Kahan summation;
	// initialize the two arrays
	if (!obs->pixerrs)
		obs->pixerrs = gsl_matrix_alloc (obs->grism->size1, obs->grism->size2);
	gsl_matrix_set_all(obs->grism,   0.0);
	gsl_matrix_set_all(obs->pixerrs, 0.0);

	// get the image dimensions
	npixels = get_npixel(obs);

	conf = get_aperture_descriptor (CONF_file);
	get_extension_numbers(grism_file, conf, conf->optkey1, conf->optval1);
	// save the fits header
	gcards = get_FITS_cards(grism_file, conf->science_numext);

	// get the  matrix with the drizzle coefficients
	drzcoeffs = get_crossdisp_matrix(grism_file, conf->science_numext);
	if (drzcoeffs->size1 < 2 || !drzcoeffs->size2)
		fprintf (stderr, "aXe_DISPIMAGE: function oblist_to_dirlist\n\
		    Could not get the drizzle coefficients in file: %s\n", grism_file);

	// determine an offset from the PSF_OFFSET
	max_offs = (int)ceil(get_max_offset(conf));

	// determine the number of objects in the object list
	nobjects = object_list_size(oblist);

	// for each object
	for (i = 0; i < nobjects; i++)
	{
		if (oblist[i]->nbeams > 0) {
			//---
			//new way to get the direct image
			if (has_aper_dirim(modim_access, oblist[i]))
				actdir = load_dirobj_img(oblist[i], modim_access);
			else
				actdir = fill_dirobject(oblist[i], npixels, drzcoeffs, 5, max_offs);
			//---

			// load the spectral values into the dirobject
			load_spectrum(oblist[i], actdir, spectrum_access, 1);

			for (beamID=0; beamID < conf->nbeams; beamID++) {
				actdir->xy_off[beamID].x = 0.0;
				actdir->xy_off[beamID].y = 0.0;
			}

			// for each beam
			for (j=0; j < oblist[i]->nbeams; j++) {
				spec=dimension_beamspec(actdir, oblist[i], npixels, conf, j);

				if (spec == NULL) {
					fprintf(stderr, "aXe_DISPIMAGE: function compute_disp\n\
				beamspec is NULL\n\
				skipping object %i beam %c ...", oblist[i]->ID, BEAM(j));
				}
				else {
					actbeam = get_beam_for_beamspec(oblist, nobjects, spec);
					if (actbeam.ignore != 1)
					{
						psf_offset = get_psf_offset(conf, actbeam);
						wl_calibration = get_calib_function(spec, actdir, CONF_file, conf);
						resp = get_throughput_spec(spec, CONF_file);
						acttrace = compute_short_tracedata(conf, actbeam, actdir, wl_calibration, spec);

						if (acttrace->npoints < 1)
						{
							fprintf(stderr, "aXe_DISPIMAGE: function compute_disp\n\
					trace is empty\n\
					skipping object %i beam %c ...", spec->objectID, BEAM(spec->beamID));
						}
						else {

							// fill the flux information into the tracedata
							fill_fluxfrom_SED(actdir, acttrace);
							fprintf(stdout, "aXe_DISPIMAGE: modelling object %i beam %c ...", spec->objectID, BEAM(spec->beamID));

							// iterate over the direct image area
							for (nx=actdir->ix_min; nx<=actdir->ix_max; nx++) {
								for (ny=actdir->iy_min; ny<=actdir->iy_max; ny++) {

									// fill the dpixel structure
									dpixel.x = (double)nx;
									dpixel.y = (double)ny;

									if (actdir->dirim)
									{
										sval = get_diremission_value(actdir->dirim, dpixel.x - actbeam.refpoint.x, dpixel.y - actbeam.refpoint.y);
										gsl_vector_set_all (acttrace->gvalue, sval);
									}
									else {
										// check whether a wavelength-dependent
										// emission profile is given
										if ((conf->psfcoeffs && conf->psfrange) || psf_offset) {
											// fill in the wavelength dependend
											// emission values
											fill_gaussvalues(dpixel, actbeam, actdir, lambda_psf, conf, psf_offset, acttrace);
										}
										else {
											// do a subsampling over the pixel
											// to get a more appropriate value for the
											// emission val
											sval = get_sub_emodel_value(dpixel, actbeam, actdir->drzscale);
											gsl_vector_set_all (acttrace->gvalue, sval);
										}
									}

									// transfer the pixel contribution to the beam spectrum
									fill_pixel_in_speed(actdir, acttrace, dpixel, resp, spec, wl_calibration);
								}
							}

							// add the beam spectrum to the simulation
							add2image(npixels, obs, spec);
						}

						// release the memory for the various structures
						fprintf(stdout, " Done\n");
						free_calib(wl_calibration);
						free_spectrum(resp);
						free_tracedata(acttrace);
						gsl_matrix_free (spec->model);
						free(spec);
					}
				}
			}
			// free the entire direct image
			free_dirobject (actdir);
		}
	}

	// write grism image and copy the FITS header
	gsl_to_FITSimage(obs->grism, grism_file, 1, "SCI");
	put_FITS_cards(grism_file, 2, gcards);

	if (oblist !=NULL)
		free_oblist (oblist);
	if (spectrum_access != NULL)
		free_fits_access(spectrum_access);
	if (modim_access!=NULL)
		free_fits_access(modim_access);
	gsl_matrix_free(drzcoeffs);
	free_FITScards(gcards);
	free_aperture_conf(conf);

	return 1;
}

/**
 * Function: add2image
 * The function add a model spectra to the grism image.
 * Uses the Kahan summation http://en.wikipedia.org/wiki/Kahan_summation_algorithm
 * in order to reduce the numerical error. The pixerrs-array of the observation struct,
 * which is not used in the simulations here, is taken to store the low-order bits.
 *
 */
int add2image(const px_point npixels, observation *obs, beamspec *spec)
{
	double y, t;
	int xact, yact;
	int ix, iy;

	// go over each pixel in the array of the beam model
	for (xact=0; xact < spec->model->size1; xact++)
	{
		for (yact=0; yact < spec->model->size2; yact++)
		{
			// find the coordinates of the pixels in the whole image model
			ix = (int)spec->model_ref.x + xact;
			iy = (int)spec->model_ref.y + yact;

			// check for safety reasons whether the coordinates are inside
			if (ix < 0 || iy < 0 || ix > (npixels.x-1) || iy > (npixels.y-1))
			{
				fprintf(stderr, "aXe_DISPIMAGE: function add2image\n\
		       object %i beam %c pixel %i,%i is outside the image\n\
		       This should not happend!!!", spec->objectID, BEAM(spec->beamID), xact, yact);
			}
			else {
				// sum up the pixels
				y = gsl_matrix_get(spec->model, xact, yact) - gsl_matrix_get(obs->pixerrs, ix, iy);
				t = gsl_matrix_get(obs->grism, ix, iy) + y;
				gsl_matrix_set(obs->pixerrs, ix, iy, (t-gsl_matrix_get(obs->grism, ix, iy))-y);
				gsl_matrix_set(obs->grism, ix, iy, t);
			}
		}
	}

	return 1;
}
