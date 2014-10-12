# Try to find gnu scientific library GSL
# This module uses the following variable 
#  GSL_ROOT_DIR
# Once done it defines the following variables
#  GSL_FOUND - system has GSL lib
#  GSL_INCLUDE_DIRS - where to find headers
#  GSL_LIBRARIES - full path to the libraries
#  GSL_LIBRARIES_DIRS, the directory where the PLplot library is found.
#  GSL_CFLAGS, additional c (c++) required
#  GSL_VERSION_STRING - Human readable version number of cfitsio
#  GSL_VERSION_MAJOR  - Major version number of cfitsio
#  GSL_VERSION_MINOR  - Minor version number of cfitsio
# Based on a script of Felix Woelk and Jan Woetzel
# (www.mip.informatik.uni-kiel.de)
# Redistribution and use is allowed according to the terms of the BSD license.

set( GSL_FOUND OFF )
set( GSL_CBLAS_FOUND OFF )

if(GSL_INCLUDE_DIRS AND GSL_LIBRARIES)
  # in cache already
  set(GSL_FIND_QUIETLY TRUE)
  message(STATUS "GSL already in cache: ${GSL_INCLUDE_DIRS} ${GSL_LIBRARIES}")

else(GSL_INCLUDE_DIRS AND GSL_LIBRARIES)

  if(UNIX)

    find_program(GSL_CONFIG_EXECUTABLE gsl-config 
      HINTS ${GSL_ROOT_DIR}
	  PATH_SUFFIXES bin gsl/bin
	  PATHS /usr/bin/ /usr/local/bin $ENV{GSL_DIR}/bin ${GSL_DIR}/bin
     )

    if(GSL_CONFIG_EXECUTABLE)
 
      set(GSL_FOUND ON)
      # run the gsl-config program to get cxxflags
      execute_process(COMMAND sh "${GSL_CONFIG_EXECUTABLE}" --cflags
        OUTPUT_VARIABLE GSL_CFLAGS
        RESULT_VARIABLE RET
        ERROR_QUIET
      )
      if(RET EQUAL 0)
        string(STRIP "${GSL_CFLAGS}" GSL_CFLAGS )
        separate_arguments(GSL_CFLAGS)
        # parse definitions from cflags; drop -D* from CFLAGS
        string(REGEX MATCHALL "-D[^;]+" GSL_DEFINITIONS "${GSL_CFLAGS}")
        string(REGEX REPLACE "-D[^;]+;" "" GSL_CFLAGS "${GSL_CFLAGS}")
        # parse include dirs from cflags; drop -I prefix
        string(REGEX MATCHALL "-I[^;]+" GSL_INCLUDE_DIRS "${GSL_CFLAGS}")
        string(REPLACE "-I" "" GSL_INCLUDE_DIRS "${GSL_INCLUDE_DIRS}")
        string(REGEX REPLACE "-I[^;]+;" "" GSL_CFLAGS "${GSL_CFLAGS}")
      else(RET EQUAL 0)
        set(GSL_FOUND FALSE)
      endif(RET EQUAL 0)
 
      # run the gsl-config program to get the libs
      execute_process(COMMAND sh "${GSL_CONFIG_EXECUTABLE}" --libs
        OUTPUT_VARIABLE GSL_LIBRARIES
        RESULT_VARIABLE RET
        ERROR_QUIET
      )
      if(RET EQUAL 0)
        string(STRIP "${GSL_LIBRARIES}" GSL_LIBRARIES)
        separate_arguments(GSL_LIBRARIES) 
        # extract linkdirs (-L) for rpath (i.e., LINK_DIRECTORIES)
        string(REGEX MATCHALL "-L[^;]+" GSL_LIBRARIES_DIRS "${GSL_LIBRARIES}")
        string(REPLACE "-L" "" GSL_LIBRARIES_DIRS "${GSL_LIBRARIES_DIRS}")
      else(RET EQUAL 0)
        set(GSL_FOUND FALSE)
      endif(RET EQUAL 0)
 
      mark_as_advanced(GSL_CFLAGS)

      if(NOT GSL_FIND_QUIETLY)
        execute_process(COMMAND sh "${GSL_CONFIG_EXECUTABLE}" --prefix
          OUTPUT_VARIABLE GSL_PREFIX OUTPUT_STRIP_TRAILING_WHITESPACE)
        #message(STATUS "Using GSL from ${GSL_PREFIX}")
      endif(NOT GSL_FIND_QUIETLY)

    else(GSL_CONFIG_EXECUTABLE)
      message(STATUS "FindGSL: gsl-config not found")
    endif(GSL_CONFIG_EXECUTABLE)

  endif(UNIX)

endif(GSL_INCLUDE_DIRS AND GSL_LIBRARIES)

if(GSL_FOUND)
  # run the gsl-config program to get the version
  execute_process(COMMAND sh "${GSL_CONFIG_EXECUTABLE}" --version
    OUTPUT_VARIABLE GSL_VERSION_STRING
    RESULT_VARIABLE RET
    ERROR_QUIET
    )
  if(RET EQUAL 0)
    string(STRIP "${GSL_VERSION_STRING}" GSL_VERSION_STRING)
    string(REGEX REPLACE ".*[^0-9]*([0-9]+)\\.([0-9]+).*" "\\1.\\2" GSL_VERSION_STRING ${GSL_VERSION_STRING})
  	string(REGEX REPLACE "^([0-9]+)[.]([0-9]+)" "\\1" GSL_VERSION_MAJOR ${GSL_VERSION_STRING})
 	string(REGEX REPLACE "^([0-9]+)[.]([0-9]+)" "\\2" GSL_VERSION_MINOR ${GSL_VERSION_STRING})
    #message(STATUS "Found GSL version ${GSL_VERSION_STRING}")
  endif(RET EQUAL 0)

  if(NOT GSL_FIND_QUIETLY)
    message(STATUS "Found GSL ${GSL_VERSION_MAJOR}.${GSL_VERSION_MINOR}: ${GSL_LIBRARIES} ${GSL_INCLUDE_DIRS} ")
  endif(NOT GSL_FIND_QUIETLY)

else(GSL_FOUND)
  if(GSL_FIND_REQUIRED)
    message(FATAL_ERROR "FindGSL: Could not find GSL headers or library" )
  endif( GSL_FIND_REQUIRED )
endif(GSL_FOUND)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(GSL DEFAULT_MSG GSL_INCLUDE_DIRS GSL_LIBRARIES)
mark_as_advanced(GSL_CONFIG_EXECUTABLE GSL_INCLUDE_DIRS GSL_LIBRARIES GSL_LIBRARIES_DIR GSL_CBLAS_LIBRARIES)

