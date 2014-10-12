# Try to find CFITSIO
# This module uses the following variable
#  CFITSIO_ROOT_DIR
# Once done this will define
#  CFITSIO_FOUND - system has CFITSIO
#  CFITSIO_INCLUDE_DIRS - the CFITSIO include directory
#  CFITSIO_LIBRARIES - Link these to use CFITSIO
#  CFITSIO_VERSION_STRING - Human readable version number of cfitsio
#  CFITSIO_VERSION_MAJOR  - Major version number of cfitsio
#  CFITSIO_VERSION_MINOR  - Minor version number of cfitsio
# Based on FindLibfacile by Carsten Niehaus, <cniehaus@gmx.de>
# Redistribution and use is allowed according to the terms of the BSD license.

set(CFITSIO_FOUND OFF)

if(CFITSIO_INCLUDE_DIRS AND CFITSIO_LIBRARIES)
  # in cache already, be quiet
  set(CFITSIO_FIND_QUIETLY TRUE)
  message(STATUS "CFITSIO already in cache: ${CFITSIO_INCLUDE_DIRS} ${CFITSIO_LIBRARIES}")

else(CFITSIO_INCLUDE_DIRS AND CFITSIO_LIBRARIES)

#  if(NOT WIN32)
#    find_package(PkgConfig)
#    if(PKG_CONFIG_FOUND)
#       pkg_check_modules(PC_CFITSIO cfitsio)
#    endif(PKG_CONFIG_FOUND)
#  endif(NOT WIN32)

  find_path(CFITSIO_INCLUDE_DIRS fitsio.h
  PATH_SUFFIXES libcfitsio3 libcfitsio0 cfitsio include cfitsio/include include/cfitsio
  HINTS ${CFITSIO_ROOT_DIR} ${PC_CFITSIO_INCLUDE_DIRS}
  PATHS $ENV{CFITSIO} ${_obIncDir} ${GNUWIN32_DIR}/include
  )

  set(CMAKE_FIND_LIBRARY_SUFFIXES .a)
  find_library(CFITSIO_STATIC_LIBRARIES NAMES cfitsio
  PATH_SUFFIXES libcfitsio3 libcfitsio0 cfitsio lib cfitsio/lib
  HINTS ${CFITSIO_ROOT_DIR} ${PC_CFITSIO_LIBRARIES}
  PATHS $ENV{CFITSIO} ${_obLinkDir} ${GNUWIN32_DIR}/lib
  )

  set(CMAKE_FIND_LIBRARY_SUFFIXES .so)
  find_library(CFITSIO_SHARED_LIBRARIES NAMES cfitsio
  PATH_SUFFIXES libcfitsio3 libcfitsio0 cfitsio lib cfitsio/lib
  HINTS ${CFITSIO_ROOT_DIR} ${PC_CFITSIO_LIBRARIES}
  PATHS $ENV{CFITSIO} ${_obLinkDir} ${GNUWIN32_DIR}/lib
  )

  if(CFITSIO_USE_STATIC)
    if(CFITSIO_STATIC_LIBRARIES)
      set(CFITSIO_LIBRARIES ${CFITSIO_STATIC_LIBRARIES})
    else(CFITSIO_STATIC_LIBRARIES)
      if(CFITSIO_SHARED_LIBRARIES)
        message(STATUS "CFITSIO was only found through a shared lib")
        set(CFITSIO_LIBRARIES ${CFITSIO_SHARED_LIBRARIES})
      else(CFITSIO_SHARED_LIBRARIES)
        message(STATUS "CFITSIO lib was not found (static nor shared)")
        set(CFITSIO_LIBRARIES ${CFITSIO_STATIC_LIBRARIES})
      endif(CFITSIO_SHARED_LIBRARIES)
    endif(CFITSIO_STATIC_LIBRARIES)  
  else(CFITSIO_USE_STATIC)
      if(CFITSIO_SHARED_LIBRARIES)
        set(CFITSIO_LIBRARIES ${CFITSIO_SHARED_LIBRARIES})
      else(CFITSIO_SHARED_LIBRARIES)
        if(CFITSIO_STATIC_LIBRARIES)
          message(STATUS "CFITSIO was only found through a static lib")
          set(CFITSIO_LIBRARIES ${CFITSIO_STATIC_LIBRARIES})
        else(CFITSIO_STATIC_LIBRARIES)
          message(STATUS "CFITSIO lib was not found (static nor shared)")
          set(CFITSIO_LIBRARIES ${CFITSIO_STATIC_LIBRARIES})
        endif(CFITSIO_STATIC_LIBRARIES)
      endif(CFITSIO_SHARED_LIBRARIES)
  endif(CFITSIO_USE_STATIC)
endif(CFITSIO_INCLUDE_DIRS AND CFITSIO_LIBRARIES)

if(CFITSIO_INCLUDE_DIRS AND CFITSIO_LIBRARIES)
  set(CFITSIO_FOUND ON)
else(CFITSIO_INCLUDE_DIRS AND CFITSIO_LIBRARIES)
  set(CFITSIO_FOUND OFF)
endif(CFITSIO_INCLUDE_DIRS AND CFITSIO_LIBRARIES)

if(CFITSIO_FOUND)
  # Find the version of the cfitsio header
  FILE(READ "${CFITSIO_INCLUDE_DIRS}/fitsio.h" FITSIO_H)
  STRING(REGEX REPLACE ".*#define CFITSIO_VERSION[^0-9]*([0-9]+)\\.([0-9]+).*" "\\1.\\2" CFITSIO_VERSION_STRING "${FITSIO_H}")
  STRING(REGEX REPLACE "^([0-9]+)[.]([0-9]+)" "\\1" CFITSIO_VERSION_MAJOR ${CFITSIO_VERSION_STRING})
  STRING(REGEX REPLACE "^([0-9]+)[.]([0-9]+)" "\\2" CFITSIO_VERSION_MINOR ${CFITSIO_VERSION_STRING})
  #message(STATUS "Found CFITSIO version ${CFITSIO_VERSION_STRING}")

  if(NOT CFITSIO_FIND_QUIETLY)
    #message(STATUS "Found CFITSIO ${CFITSIO_VERSION_MAJOR}.${CFITSIO_VERSION_MINOR}: ${CFITSIO_LIBRARIES} ${CFITSIO_INCLUDE_DIRS} ")
  endif(NOT CFITSIO_FIND_QUIETLY)

else(CFITSIO_FOUND)
  if(CFITSIO_FIND_REQUIRED)
    message(FATAL_ERROR "FindCFITSIO: Could not find CFITSIO headers or library")
  endif(CFITSIO_FIND_REQUIRED)
endif(CFITSIO_FOUND)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CFITSIO DEFAULT_MSG CFITSIO_INCLUDE_DIRS CFITSIO_LIBRARIES)
mark_as_advanced(CFITSIO_INCLUDE_DIRS CFITSIO_LIBRARIES)


