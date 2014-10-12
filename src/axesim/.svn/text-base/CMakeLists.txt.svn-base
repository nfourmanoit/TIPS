message(STATUS "Building aXeSIM")

# INCLUDES
find_package(CFITSIO REQUIRED)
if(CFITSIO_FOUND)
        include_directories(${CFITSIO_INCLUDE_DIRS})
endif(CFITSIO_FOUND)
find_package(GSL REQUIRED)
if(GSL_FOUND)
        include_directories(${GSL_INCLUDE_DIR})
endif(GSL_FOUND)
find_package(WCSLIB REQUIRED)
if(WCSLIB_FOUND)
        include_directories(${WCSLIB_INCLUDE_DIR})
endif(WCSLIB_FOUND)

# AXESIM LIB
file(GLOB AXESIM_SOURCES ${SRC_DIR}/axesim/*.c) 
#file(GLOB AXESIM_HEADERS ${SRC_DIR}/axesim/*.h)
include_directories(${SRC_DIR}/axesim)
#set(AXESIM_SOURCES ${AXESIM_CSOURCES} ${AXESIM_HEADERS})
set(AXESIM_EXECUTABLES aXe_SEX2GOL aXe_GOL2AF aXe_AF2PET aXe_PET2SPC aXe_STAMPS aXe_PETCONT aXe_DIRIMAGE aXe_DISPIMAGE)
foreach(EXE ${AXESIM_EXECUTABLES})
	add_executable(${EXE} ${AXESIM_SOURCES})
	target_link_libraries(${EXE} ${CFITSIO_LIBRARIES} ${GSL_LIBRARIES})
	message(STATUS "${EXE}": built)
endforeach()

# INSTALL
#install (TARGETS PHD RUNTIME DESTINATION bin)
