/**
 * The interface ti the Pixel extraction table input/output routines
 *
 * @author  Martin Kuemmel, Nor Pirzkal
 * @package spce_PET
 * @version $Revision: 1.3 $
 * @date    $Date: 2009/09/21 12:46:17 $
 */

#ifndef _SPCE_PET_H

#define _SPCE_PET_H

extern ap_pixel *
alloc_aperture_table (long N);

extern void
create_PET (char filename[], int overwrite);

extern fitsfile *
create_PET_opened (char filename[], int overwrite);

extern long 
PET_count_elements (ap_pixel * ap_p);

extern int
get_PET_colnum (fitsfile * input, char colname[]);

extern void
add_ALL_to_PET (ap_pixel * ap_p, char ID[], fitsfile *input, int update);

extern ap_pixel *
get_ALL_from_next_in_PET(fitsfile *input, int *aperID, int *beamID);

extern void
fprintf_ap_pixel (FILE * output, ap_pixel ap);

extern void
fprintf_ap_pixel_list (FILE * output, ap_pixel * ap);

#endif
