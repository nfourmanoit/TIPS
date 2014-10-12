message(STATUS "Building aXeSIM")

# DEPENDENCIES
#set(CFITSIO_USE_STATIC ON)
find_package(CFITSIO REQUIRED QUIET)
if(CFITSIO_FOUND)
    message(STATUS "Found CFITSIO ${CFITSIO_VERSION_MAJOR}.${CFITSIO_VERSION_MINOR}: ${CFITSIO_INCLUDE_DIRS} ${CFITSIO_LIBRARIES}")
    include_directories(${CFITSIO_INCLUDE_DIRS})
endif(CFITSIO_FOUND)
#set(GSL_USE_STATIC ON)
find_package(GSL REQUIRED QUIET)
if(GSL_FOUND)
    message(STATUS "Found GSL ${GSL_VERSION_MAJOR}.${GSL_VERSION_MINOR}: ${GSL_INCLUDE_DIRS} ${GSL_LIBRARIES}")
    include_directories(${GSL_INCLUDE_DIRS})
endif(GSL_FOUND)
set(WCSLIB_USE_STATIC ON)
find_package(WCSLIB REQUIRED QUIET)
if(WCSLIB_FOUND)
    message(STATUS "Found WCSLIB ${WCSLIB_VERSION_MAJOR}.${WCSLIB_VERSION_MINOR}: ${WCSLIB_INCLUDE_DIRS} ${WCSLIB_LIBRARIES}")
    include_directories(${WCSLIB_INCLUDE_DIRS})
endif(WCSLIB_FOUND)

# SOURCES
include_directories(${INC_DIR}/axesim)
set(AXESIM_SOURCES
 ${SRC_DIR}/axesim/aper_check.c
 ${SRC_DIR}/axesim/aper_conf.c
 ${SRC_DIR}/axesim/aXe_errors.c
 ${SRC_DIR}/axesim/aXe_utils.c
 ${SRC_DIR}/axesim/crossdisp_utils.c
 ${SRC_DIR}/axesim/dirimage_model.c
 ${SRC_DIR}/axesim/disp_conf.c
 ${SRC_DIR}/axesim/disp_utils.c
 ${SRC_DIR}/axesim/drizzle_utils.c
 ${SRC_DIR}/axesim/drz2pet_utils.c
 ${SRC_DIR}/axesim/fringe_conf.c
 ${SRC_DIR}/axesim/fringe_model.c
 ${SRC_DIR}/axesim/fringe_utils.c
 ${SRC_DIR}/axesim/inima_utils.c
 ${SRC_DIR}/axesim/inout_aper.c
 ${SRC_DIR}/axesim/ipixcorr_utils.c
 ${SRC_DIR}/axesim/lmmin.c
 ${SRC_DIR}/axesim/lm_eval.c
 ${SRC_DIR}/axesim/nicback_utils.c
 ${SRC_DIR}/axesim/model_utils.c
 ${SRC_DIR}/axesim/specmodel_utils.c
 ${SRC_DIR}/axesim/spce_binning.c
 ${SRC_DIR}/axesim/spce_fitting.c
 ${SRC_DIR}/axesim/spce_is_in.c
 ${SRC_DIR}/axesim/spce_pathlength.c
 ${SRC_DIR}/axesim/spce_sect.c
 ${SRC_DIR}/axesim/spce_output.c
 ${SRC_DIR}/axesim/spce_PET.c
 ${SRC_DIR}/axesim/spc_back.c
 ${SRC_DIR}/axesim/spc_CD.c
 ${SRC_DIR}/axesim/spc_cfg.c
 ${SRC_DIR}/axesim/spc_driz.c
 ${SRC_DIR}/axesim/spc_extract.c
 ${SRC_DIR}/axesim/spc_FITScards.c
 ${SRC_DIR}/axesim/spc_flatfield.c
 ${SRC_DIR}/axesim/spc_fluxcube.c
 ${SRC_DIR}/axesim/spc_model.c
 ${SRC_DIR}/axesim/spc_optimum.c
 ${SRC_DIR}/axesim/spc_resp.c
 ${SRC_DIR}/axesim/spc_sex.c
 ${SRC_DIR}/axesim/spc_spc.c
 ${SRC_DIR}/axesim/spc_trace_functions.c
 ${SRC_DIR}/axesim/spc_utils.c
 ${SRC_DIR}/axesim/spc_wl_calib.c
 ${SRC_DIR}/axesim/trace_conf.c
 ${SRC_DIR}/axesim/trfit_utils.c
)

set(AXESIM_HEADERS 
 ${INC_DIR}/axesim/aper_check.h
 ${INC_DIR}/axesim/aper_conf.h
 ${INC_DIR}/axesim/aXe_errors.h
 ${INC_DIR}/axesim/aXe_grism.h
 ${INC_DIR}/axesim/aXe_utils.h
 ${INC_DIR}/axesim/crossdisp_utils.h
 ${INC_DIR}/axesim/dirimage_model.h
 ${INC_DIR}/axesim/disp_conf.h
 ${INC_DIR}/axesim/disp_utils.h
 ${INC_DIR}/axesim/drizzle_utils.h
 ${INC_DIR}/axesim/drz2pet_utils.h
 ${INC_DIR}/axesim/fringe_conf.h
 ${INC_DIR}/axesim/fringe_model.h
 ${INC_DIR}/axesim/fringe_utils.h
 ${INC_DIR}/axesim/inima_utils.h
 ${INC_DIR}/axesim/inout_aper.h
 ${INC_DIR}/axesim/ipixcorr_utils.h
 ${INC_DIR}/axesim/lm_eval.h
 ${INC_DIR}/axesim/lmmin.h
 ${INC_DIR}/axesim/model_utils.h
 ${INC_DIR}/axesim/nicback_utils.h
 ${INC_DIR}/axesim/spc_back.h
 ${INC_DIR}/axesim/spc_CD.h
 ${INC_DIR}/axesim/spc_cfg.h
 ${INC_DIR}/axesim/spc_driz.h
 ${INC_DIR}/axesim/spce_binning.h
 ${INC_DIR}/axesim/spce_fitting.h
 ${INC_DIR}/axesim/spce_is_in.h
 ${INC_DIR}/axesim/spce_output.h
 ${INC_DIR}/axesim/spce_pathlength.h
 ${INC_DIR}/axesim/spce_PET.h
 ${INC_DIR}/axesim/spce_sect.h
 ${INC_DIR}/axesim/spc_FITScards.h
 ${INC_DIR}/axesim/spc_flatfield.h
 ${INC_DIR}/axesim/spc_fluxcube.h
 ${INC_DIR}/axesim/spc_model.h
 ${INC_DIR}/axesim/spc_optimum.h
 ${INC_DIR}/axesim/spc_resp.h
 ${INC_DIR}/axesim/spc_sex.h
 ${INC_DIR}/axesim/spc_spc.h
 ${INC_DIR}/axesim/spc_trace_functions.h
 ${INC_DIR}/axesim/spc_utils.h
 ${INC_DIR}/axesim/spc_wl_calib.h
 ${INC_DIR}/axesim/specmodel_utils.h
 ${INC_DIR}/axesim/trace_conf.h
 ${INC_DIR}/axesim/trfit_utils.h
)

# LIBRARY
add_library(axesim_STATIC STATIC ${AXESIM_SOURCES} ${AXESIM_HEADERS})
add_library(axesim_SHARED SHARED ${AXESIM_SOURCES} ${AXESIM_HEADERS})

#set(AXESIM_LIBS ${axesim_SHARED} ${CFITSIO_LIBRARIES} ${GSL_LIBRARIES} ${WCSLIB_LIBRARIES})
set(AXESIM_LIBS ${CFITSIO_LIBRARIES} ${GSL_LIBRARIES} ${WCSLIB_LIBRARIES})

# EXECUTABLES
set(AXESIM_EXECUTABLES aXe_SEX2GOL aXe_GOL2AF aXe_AF2PET aXe_PET2SPC aXe_STAMPS aXe_PETCONT aXe_DIRIMAGE aXe_DISPIMAGE)
foreach(EXE ${AXESIM_EXECUTABLES})
    set(EXE_SOURCE "${SRC_DIR}/axesim/${EXE}.c")
    add_executable(${EXE} ${EXE_SOURCE} ${AXESIM_SOURCES} ${AXESIM_HEADERS} )
    target_link_libraries(${EXE} ${AXESIM_LIBS})
    message(STATUS "${EXE}": done)
endforeach()
# INSTALL
#install (TARGETS)
