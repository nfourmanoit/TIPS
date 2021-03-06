# CMake Wrapper Makefile

SHELL := /bin/bash
RM    := rm -rf

all: ./build/Makefile
	@ $(MAKE) -C build

./build/Makefile:
	@ (cd build >/dev/null 2>&1 && cmake ..)

distclean:
	@- (cd build >/dev/null 2>&1 && cmake .. >/dev/null 2>&1)
	@- $(MAKE) -C build clean || true
	@- $(RM) ./build/*
	@- $(RM) ./doc/*
	@- $(RM) ./*~
	@- $(RM) ./Makefile

ifeq ($(findstring distclean,$(MAKECMDGOALS)),)
    $(MAKECMDGOALS): ./build/Makefile
	@ $(MAKE) -C build $(MAKECMDGOALS)
endif

