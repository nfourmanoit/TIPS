/*
    aXe_DISPIMAGE
    $Revision: 1.0 $ $Date: 2010/05/20 10:35:43 $
    Martin Kuemmel
    Julien Zoubian

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "aXe_grism.h"
#include "aXe_utils.h"
#include "aper_conf.h"
#include "spce_output.h"
#include "disp_utils.h"

#define AXE_IMAGE_PATH "AXE_IMAGE_PATH"
#define AXE_OUTPUT_PATH "AXE_OUTPUT_PATH"
#define AXE_CONFIG_PATH "AXE_CONFIG_PATH"

int
main (int argc, char *argv[])
{
  char *opt;
  char aper_file[MAXCHAR];
  char aper_file_path[MAXCHAR];

  char conf_file[MAXCHAR];
  char conf_file_path[MAXCHAR];

  char grism_file[MAXCHAR];
  char grism_file_path[MAXCHAR];

  char specmod_file[MAXCHAR];
  char specmod_file_path[MAXCHAR];

  char objmod_file[MAXCHAR];
  char objmod_file_path[MAXCHAR];

  aperture_conf *conf;

  int index;
  double lambda_psf=0.0;

  observation *obs;

  if ((argc < 3) || (opt = get_online_option ("help", argc, argv)))
    {
      fprintf (stdout,
    		  "Usage:\n"
    		  "      aXe_DISPIMAGE g/prism_filename configuration_filename"
    		  "\n"
    		  "Options:\n"
    		  "      -in_AF=[string]         - overwrite the automatically generated name\n"
    		  "                                of the input aperture file\n"
    		  "      -model_spectra=[string] - input model spectra"
    		  "      -model_images=[string]  - input model images"
    		  "      -lambda_psf=[float]     - lambda at which psf was measured"
    		  "\n",RELEASE);
      exit (1);
    }

  fprintf (stdout, "aXe_DISPIMAGE: Starting...\n");

  index = 0;

  strcpy (grism_file, argv[++index]);
  build_path (AXE_IMAGE_PATH, grism_file, grism_file_path);

  strcpy (conf_file, argv[++index]);
  build_path (AXE_CONFIG_PATH, conf_file, conf_file_path);

  conf = get_aperture_descriptor (conf_file_path);
  get_extension_numbers(grism_file_path, conf,conf->optkey1,conf->optval1);

 /* Get or set up the name of the output Aperture File */
  if ((opt = get_online_option ("in_AF", argc, argv)))
    {
      /* get it */
      strcpy (aper_file, opt);
      strcpy (aper_file_path, opt);
    }
  else {
    /* Build aperture file name */
    replace_file_extension (grism_file, aper_file, ".fits",
			    ".OAF", conf->science_numext);
    build_path (AXE_OUTPUT_PATH, aper_file, aper_file_path);
  }

  // determine the wavelength
  // the object extend was determined at
  if ((opt = get_online_option ("lambda_psf", argc, argv)))
    lambda_psf = atof(opt);
  else
    lambda_psf = 800.0;

  // check whether a name for the spectral
  // models file is given
  if ((opt = get_online_option ("model_spectra", argc, argv)))
    {
      // get and set up the filename
      strcpy (specmod_file, opt);
      build_path (AXE_IMAGE_PATH, specmod_file, specmod_file_path);
    }
  else
    {
      strcpy (specmod_file, "");
      strcpy (specmod_file_path, "");
    }
  
  // check whether a name for the images
  // models file is given
  if ((opt = get_online_option ("model_images", argc, argv)))
    {
      // get and set up the filename
      strcpy (objmod_file, opt);
      build_path (AXE_IMAGE_PATH, objmod_file, objmod_file_path);
    }
  else
    {
      strcpy (objmod_file, "");
      strcpy (objmod_file_path, "");
    }

  fprintf (stdout, "aXe_DISPIMAGE: grism image file name: %s\n", grism_file_path);
  fprintf (stdout, "aXe_DISPIMAGE: Input Aperture file name: %s\n", aper_file_path);
  fprintf (stdout, "aXe_DISPIMAGE: Using spectral models in table: %s\n", specmod_file_path);
  fprintf (stdout, "aXe_DISPIMAGE: Using direct emission objects in image: %s\n", objmod_file_path);
  fprintf (stdout, "aXe_DISPIMAGE: Object parameters determined at %fnm\n", lambda_psf);

  fprintf (stdout, "aXe_DISPIMAGE: ");
  obs = load_sci_image (grism_file_path, conf->science_numext);

  compute_disp(grism_file_path, aper_file_path, conf_file_path,
		       specmod_file_path,  objmod_file_path, lambda_psf, obs);

  free_observation(obs);
  free_aperture_conf(conf);
  fprintf (stdout, "aXe_DISPIMAGE: Done...\n");
  exit (0);
}
