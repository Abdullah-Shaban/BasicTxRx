INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_CREW crew)

FIND_PATH(
    CREW_INCLUDE_DIRS
    NAMES crew/api.h
    HINTS $ENV{CREW_DIR}/include
        ${PC_CREW_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    CREW_LIBRARIES
    NAMES gnuradio-crew
    HINTS $ENV{CREW_DIR}/lib
        ${PC_CREW_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CREW DEFAULT_MSG CREW_LIBRARIES CREW_INCLUDE_DIRS)
MARK_AS_ADVANCED(CREW_LIBRARIES CREW_INCLUDE_DIRS)

