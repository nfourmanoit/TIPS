cmake_minimum_required (VERSION 2.6 FATAL_ERROR)
# cmake_policy(SET CMP0012 NEW)

# PROJECT
project (TIPS)
set(PROJECT_VERSION_MAJOR 1)
set(PROJECT_VERSION_MINOR 2) 
set(PROJECT_VERSION_PATCH 1)
set(PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")

# TREE
set(SRC_DIR "${PROJECT_SOURCE_DIR}/src")
set(INC_DIR "${PROJECT_SOURCE_DIR}/include") 
set(BUILD_DIR "${PROJECT_SOURCE_DIR}/build")
set(THIRD_DIR "${PROJECT_SOURCE_DIR}/thirdparty")
set(LIB_DIR "${PROJECT_SOURCE_DIR}/lib") 
set(BIN_DIR "${PROJECT_SOURCE_DIR}/bin")
set(TEST_DIR "${PROJECT_SOURCE_DIR}/test")
set(DOC_DIR "${PROJECT_SOURCE_DIR}/doc")
set(CHECKED_DIRS ${INC_DIR} ${BUILD_DIR} ${THIRD_DIR} ${LIB_DIR} ${BIN_DIR} ${TEST_DIR} ${DOC_DIR})
foreach(dir ${CHECKED_DIRS})
    if(NOT EXISTS "${dir}")
        file(MAKE_DIRECTORY "${dir}")
    endif()
endforeach(dir)
#set(EXECUTABLE_OUTPUT_PATH $BIN_DIR})
#set(LIBRARY_OUTPUT_PATH $LIB_DIR})
set(HEADER_OUTPUT_PATH ${INC_DIR})
#set(CMAKE_INCLUDE_CURRENT_DIR ON) 
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${BIN_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${LIB_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${LIB_DIR})
set(CMAKE_PREFIX_PATH ${THIRD_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/modules)

# COMPILER
set(CMAKE_COLOR_MAKEFILE ON)
set(CMAKE_VERBOSE_MAKEFILE ON)
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug) 
endif(NOT CMAKE_BUILD_TYPE)
message(STATUS "Configured for \"${CMAKE_BUILD_TYPE}\" build type")
include(CheckCCompilerFlag)
set(CFLAGS_WARNING "-pedantic" "-Wall" "-Wextra" "-Wfatal-errors")
set(CFLAGS_DEBUG "-g")
#set(CFLAGS_DEBUG "-g" "-ftime-report" "-fmem-report")
set(CFLAGS_OPTIMIZE "-O2")
set(CMAKE_C_FLAGS_DEBUG "")
set(CMAKE_C_FLAGS_RELEASE "")
foreach(flag ${CFLAGS_WARNING} ${CFLAGS_DEBUG})
    if(DEFINED FLAG_SUPPORT)
      unset(FLAG_SUPPORT CACHE)
    endif()
    check_c_compiler_flag(${flag} FLAG_SUPPORT)
    #message(STATUS "${flag} ${FLAG_SUPPORT}")
    if(FLAG_SUPPORT)
        set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} ${flag}")
    endif(FLAG_SUPPORT)
endforeach(flag)
foreach(flag ${CFLAGS_OPTIMIZE})
    check_c_compiler_flag(${flag} FLAG_SUPPORT)
    if(FLAG_SUPPORT)
        set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} ${flag}")
    endif(FLAG_SUPPORT)
endforeach(flag)
set(CMAKE_CXX_FLAGS_DEBUG ${CMAKE_C_FLAGS_DEBUG})
set(CMAKE_CXX_FLAGS_RELEASE ${CMAKE_C_FLAGS_RELEASE})

# BUILD
add_subdirectory(${SRC_DIR}/axesim ${BUILD_DIR}/axesim )

# TEST
#include(CTest)
#enable_testing()
#if(TESTING)
#  add_subdirectory(${SRC_ROOT}/test ${TEST_ROOT})
#endif(TESTING)
# add_test(NAME <name> [CONFIGURATIONS [Debug|Release|...]]
#           [WORKING_DIRECTORY dir]
#            COMMAND <command> [arg1 [arg2 ...]])


# API DOCUMENTATION
find_package(Doxygen)
option(BUILD_DOCUMENTATION "Generate API documentation (requires Doxygen)" ${DOXYGEN_FOUND})
if(BUILD_DOCUMENTATION)
  set(DOXYFILE_IN ${PROJECT_SOURCE_DIR}/Doxyfile.in)
  set(DOXYFILE ${PROJECT_SOURCE_DIR}/Doxyfile) 
  set(DOXY_HTML_INDEX ${DOC_DIR}/html/index.html)
  set(DOXY_OUTPUT_ROOT ${CMAKE_CURRENT_BINARY_DIR}) # Pasted into Doxyfile.in
  set(DOXY_INPUT ${PROJECT_SOURCE_DIR}/src) # Pasted into Doxyfile.in
  set(DOXY_EXTRA_FILES ${CMAKE_CURRENT_SOURCE_DIR}/mainpage.dox) # Pasted into Doxyfile.in
  if(EXISTS ${DOXYFILE})
    configure_file(${DOXYFILE_IN} ${DOXYFILE} @ONLY)
    message(STATUS "Doxyfile configured")
    add_custom_target(doc
    COMMAND ${CMAKE_COMMAND} -E echo_append "Building API Documentation..."
    COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYFILE}
    MAIN_DEPENDENCY ${doxyfile} ${DOXYFILE}
    COMMAND ${CMAKE_COMMAND} -E echo "Done."
    WORKING_DIRECTORY ${DOC_DIR} 
    VERBATIM
    )

#    add_custom_command(OUTPUT ${DOXY_HTML_INDEX}
#    COMMAND ${CMAKE_COMMAND} -E echo_append "Building API Documentation..."
#    COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYFILE}
#    MAIN_DEPENDENCY ${doxyfile} ${DOXYFILE}
#    COMMAND ${CMAKE_COMMAND} -E echo "Done."
#    WORKING_DIRECTORY ${DOC_DIR} 
#    VERBATIM
#    )
##    add_custom_target(doc ALL DEPENDS ${doxy_html_index_file})
#  INSTALL( DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/html DESTINATION share/doc )

  else(EXISTS ${DOXYFILE})
    message(STATUS "${DOXYFILE_IN} does not exist") 
  endif(EXISTS ${DOXYFILE})
else(BUILD_DOCUMENTATION)
  message(STATUS "Doxygen is not found. Install it and retry.") 
endif(BUILD_DOCUMENTATION)

# PACKAGING
#include(CPack)
#set(CPACK_GENERATOR "DEB")
#set(CPACK_PACKAGE_NAME "${PROJECT_NAME}")
#set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")
#set(CPACK_PACKAGE_CONTACT "Nicolas Fourmanoit") #required
#set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "A pixel simulator for EUCLID Near Infrared Spectrometer")

# MISC
#set(CONFIGURED_ONCE TRUE CACHE INTERNAL "CMake has configured at least once.")
