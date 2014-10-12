# Try to find WCSLIB
# This module uses the following variable
#  WCSLIB_ROOT_DIR
# It will define 
#  WCSLIB_FOUND - system has WCSLIB
#  WCSLIB_INCLUDE_DIRS - the WCSLIB include directory
#  WCSLIB_LIBRARIES - Link these to use WCSLIB
# Based on FindLibfacile by Carsten Niehaus, <cniehaus@gmx.de>
# Redistribution and use is allowed according to the terms of the BSD license

set (WCSLIB_FOUND OFF)

if(WCSLIB_INCLUDE_DIRS AND WCSLIB_LIBRARIES)
  # in cache already
  set(WCSLIB_FIND_QUIETLY TRUE)
  message(STATUS "WCSLIB already in cache: ${WCSLIB_LIBRARIES} ${WCSLIB_INCLUDE_DIRS}")

else(WCSLIB_INCLUDE_DIRS AND WCSLIB_LIBRARIES)

#  if(NOT WIN32)
#    find_package(PkgConfig)
#    if(PKG_CONFIG_FOUND)
#      pkg_check_modules(PC_WCSLIB wcs)
#    endif(PKG_CONFIG_FOUND)
#  endif(NOT WIN32)

  find_path(WCSLIB_INCLUDE_DIRS wcs.h
  PATH_SUFFIXES wcs libwcs wcs/libwcs
  HINTS ${WCSLIB_ROOT_DIR} ${PC_WCSLIB_INCLUDE_DIRS}
  PATHS $ENV{WCSLIB} ${_obIncDir} ${GNUWIN32_DIR}/include
  )

  set(CMAKE_FIND_LIBRARY_SUFFIXES .a)
  find_library(WCSLIB_STATIC_LIBRARIES NAMES wcs
  PATH_SUFFIXES wcs libwcs wcs/libwcs
  HINTS ${WCSLIB_ROOT_DIR} ${PC_WCSLIB_LIBRARIES}
  PATHS $ENV{WCSLIB} ${_obLinkDir} ${GNUWIN32_DIR}/lib
  )

  set(CMAKE_FIND_LIBRARY_SUFFIXES .so)
  find_library(WCSLIB_SHARED_LIBRARIES NAMES wcs
  PATH_SUFFIXES wcs libwcs wcs/libwcs
  HINTS ${WCSLIB_ROOT_DIR} ${PC_WCSLIB_LIBRARIES}
  PATHS $ENV{WCSLIB} ${_obLinkDir} ${GNUWIN32_DIR}/lib
  )

  if(WCSLIB_USE_STATIC)
    if(WCSLIB_STATIC_LIBRARIES)
      set(WCSLIB_LIBRARIES ${WCSLIB_STATIC_LIBRARIES})
    else(WCSLIB_STATIC_LIBRARIES)
      if(WCSLIB_SHARED_LIBRARIES)
        message(STATUS "WCSLIB was only found through a shared lib")
        set(WCSLIB_LIBRARIES ${WCSLIB_SHARED_LIBRARIES})
      else(WCSLIB_SHARED_LIBRARIES)
        message(STATUS "WCSLIB lib was not found (static nor shared)")
        set(WCSLIB_LIBRARIES ${WCSLIB_STATIC_LIBRARIES})
      endif(WCSLIB_SHARED_LIBRARIES)
    endif(WCSLIB_STATIC_LIBRARIES)  
  else(WCSLIB_USE_STATIC)
      if(WCSLIB_SHARED_LIBRARIES)
        set(WCSLIB_LIBRARIES ${WCSLIB_SHARED_LIBRARIES})
      else(WCSLIB_SHARED_LIBRARIES)
        if(WCSLIB_STATIC_LIBRARIES)
          message(STATUS "WCSLIB was only found through a static lib")
          set(WCSLIB_LIBRARIES ${WCSLIB_STATIC_LIBRARIES})
        else(WCSLIB_STATIC_LIBRARIES)
          message(STATUS "WCSLIB lib was not found (static nor shared)")
          set(WCSLIB_LIBRARIES ${WCSLIB_STATIC_LIBRARIES})
        endif(WCSLIB_STATIC_LIBRARIES)
      endif(WCSLIB_SHARED_LIBRARIES)
  endif(WCSLIB_USE_STATIC)
endif(WCSLIB_INCLUDE_DIRS AND WCSLIB_LIBRARIES)

if(WCSLIB_INCLUDE_DIRS AND WCSLIB_LIBRARIES)
  set(WCSLIB_FOUND ON)
else(WCSLIB_INCLUDE_DIRS AND WCSLIB_LIBRARIES)
  set(WCSLIB_FOUND OFF)
endif(WCSLIB_INCLUDE_DIRS AND WCSLIB_LIBRARIES)

if(WCSLIB_FOUND)
  if(NOT WCSLIB_FIND_QUIETLY)
    #message(STATUS "Found WCSLIB tot: ${WCSLIB_INCLUDE_DIRS} ${WCSLIB_LIBRARIES}")
  endif(NOT WCSLIB_FIND_QUIETLY)
else(WCSLIB_FOUND)
  if(WCSLIB_FIND_REQUIRED)
    message(FATAL_ERROR "WCSLIB not found. Please install wcslib and try again.")
  endif(WCSLIB_FIND_REQUIRED)
endif(WCSLIB_FOUND)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(WCSLIB DEFAULT_MSG WCSLIB_INCLUDE_DIRS WCSLIB_LIBRARIES)
mark_as_advanced(WCSLIB_INCLUDE_DIRS WCSLIB_LIBRARIES)

