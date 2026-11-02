# ============================================================================
#  Thesis build system
#
#  Layout this Makefile expects:
#    core/      ygopro-core (git submodule)       -> libocgcore.so + headers
#    scripts/   ProjectIgnis/CardScripts           -> card Lua scripts
#    cdb/       ProjectIgnis/BabelCDB              -> card databases (SQLite)
#    src/       your shared code (NO main() here)  -> readers, parser, search...
#    app/       one .c file per program, each with its own main()
#
#  Common commands:
#    make                  build everything (release)
#    make MODE=debug       no optimisation, full debug info
#    make MODE=asan        debug + AddressSanitizer/UBSan (catches memory bugs)
#    make run APP=version  build and run app/version.c
#    make core             (re)build only the engine
#    make data             clone card scripts + databases if missing
#    make versions         print the exact commits you are building against
#    make compdb           compile_commands.json for clangd (needs `bear`)
#    make clean            remove your build output
#    make distclean        also remove the engine's build output
# ============================================================================

# ---- Configuration ---------------------------------------------------------

MODE ?= release

CORE_DIR    := core
SCRIPTS_DIR := scripts
CDB_DIR     := cdb
SRC_DIR     := src
APP_DIR     := app
BUILD_DIR   := build/$(MODE)

# premake5: use the one in PATH, else the one the core's script downloads.
PREMAKE ?= $(shell command -v premake5 2>/dev/null || echo ./premake5)

CC ?= gcc

# ---- Mode-dependent settings -----------------------------------------------
# Which engine build to link against, and which flags to use for our own code.

ifeq ($(MODE),release)
  CORE_CFG  := release
  MODEFLAGS := -O2 -g -DNDEBUG
else ifeq ($(MODE),debug)
  CORE_CFG  := debug
  MODEFLAGS := -O0 -g3
else ifeq ($(MODE),asan)
  CORE_CFG  := debug
  MODEFLAGS := -O1 -g3 -fno-omit-frame-pointer -fsanitize=address,undefined
else
  $(error Unknown MODE '$(MODE)'. Use release, debug or asan)
endif

CORE_LIBDIR := $(CORE_DIR)/bin/$(CORE_CFG)
CORE_LIB    := $(CORE_LIBDIR)/libocgcore.so

# ---- Flags -----------------------------------------------------------------

WARNINGS := -Wall -Wextra -Wpedantic -Wshadow -Wstrict-prototypes \
            -Wmissing-prototypes -Wformat=2 -Wnull-dereference

# Data locations are baked in as defaults; your code can still override them
# at runtime (e.g. from argv). $(CURDIR) makes them absolute.
DEFINES := -DYGO_SCRIPTS_DIR='"$(CURDIR)/$(SCRIPTS_DIR)"' \
           -DYGO_CDB_DIR='"$(CURDIR)/$(CDB_DIR)"'

CPPFLAGS += -I$(CORE_DIR) -I$(SRC_DIR) $(DEFINES) \
            $(shell pkg-config --cflags sqlite3)

# -MMD -MP: write .d files so editing a header rebuilds what includes it.
CFLAGS   += -std=c11 $(MODEFLAGS) $(WARNINGS) -fopenmp -MMD -MP

# rpath with $ORIGIN: the binary finds libocgcore.so relative to itself,
# so you never need LD_LIBRARY_PATH and the project folder can be moved.
LDFLAGS  += $(MODEFLAGS) -fopenmp -L$(CORE_LIBDIR) \
            -Wl,-rpath,'$$ORIGIN/../../$(CORE_LIBDIR)'
LDLIBS   += -locgcore $(shell pkg-config --libs sqlite3) -lm

# ---- Sources ---------------------------------------------------------------

SRC_FILES := $(wildcard $(SRC_DIR)/*.c)
APP_FILES := $(wildcard $(APP_DIR)/*.c)

SRC_OBJS  := $(SRC_FILES:%.c=$(BUILD_DIR)/%.o)
APP_OBJS  := $(APP_FILES:%.c=$(BUILD_DIR)/%.o)
APPS      := $(APP_FILES:$(APP_DIR)/%.c=$(BUILD_DIR)/%)

DEPS      := $(SRC_OBJS:.o=.d) $(APP_OBJS:.o=.d)

# ---- Targets ---------------------------------------------------------------

.PHONY: all core run data versions compdb clean distclean help

all: $(APPS)

# Every app links against all shared code in src/.
$(BUILD_DIR)/%: $(BUILD_DIR)/$(APP_DIR)/%.o $(SRC_OBJS) $(CORE_LIB)
	$(CC) $(LDFLAGS) -o $@ $< $(SRC_OBJS) $(LDLIBS)

# Objects. The `| dir` part creates output folders without forcing rebuilds.
$(BUILD_DIR)/%.o: %.c | $(CORE_DIR)/ocgapi.h
	@mkdir -p $(dir $@)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ $<

# Rebuild if the Makefile itself changes (flags may have changed).
$(SRC_OBJS) $(APP_OBJS): Makefile

# ---- Engine ----------------------------------------------------------------

core: $(CORE_LIB)

$(CORE_DIR)/ocgapi.h $(CORE_DIR)/lua/src/lua.h:
	git submodule update --init --recursive

$(CORE_DIR)/build/Makefile: $(CORE_DIR)/premake5.lua $(CORE_DIR)/lua/src/lua.h
	cd $(CORE_DIR) && $(PREMAKE) gmake2

# FORCE: always ask the engine's own build whether it is up to date. It is
# incremental, so this is instant when nothing changed, but it means edits
# to the engine itself (e.g. instrumentation for your thesis) get picked up.
$(CORE_LIB): $(CORE_DIR)/build/Makefile FORCE
	@$(MAKE) --no-print-directory -C $(CORE_DIR)/build ocgcoreshared config=$(CORE_CFG)

FORCE:

# ---- Run -------------------------------------------------------------------

APP ?= version
run: $(BUILD_DIR)/$(APP)
	./$(BUILD_DIR)/$(APP) $(ARGS)

# ---- Card data -------------------------------------------------------------

data: $(SCRIPTS_DIR)/constant.lua $(CDB_DIR)/cards.cdb

$(SCRIPTS_DIR)/constant.lua:
	git clone --depth 1 https://github.com/ProjectIgnis/CardScripts.git $(SCRIPTS_DIR)

$(CDB_DIR)/cards.cdb:
	git clone --depth 1 https://github.com/ProjectIgnis/BabelCDB.git $(CDB_DIR)

# For your thesis: record this output alongside every experiment.
versions:
	@printf 'core     %s\n' "$$(git -C $(CORE_DIR)    rev-parse --short HEAD 2>/dev/null || echo '?')"
	@printf 'lua      %s\n' "$$(git -C $(CORE_DIR)/lua/src rev-parse --short HEAD 2>/dev/null || echo '?')"
	@printf 'scripts  %s\n' "$$(git -C $(SCRIPTS_DIR) rev-parse --short HEAD 2>/dev/null || echo '?')"
	@printf 'cdb      %s\n' "$$(git -C $(CDB_DIR)     rev-parse --short HEAD 2>/dev/null || echo '?')"
	@printf 'compiler %s\n' "$$($(CC) --version | head -n1)"

# ---- Tooling ---------------------------------------------------------------

compdb:
	$(MAKE) clean
	bear -- $(MAKE) all

clean:
	rm -rf build

distclean: clean
	rm -rf $(CORE_DIR)/build $(CORE_DIR)/bin $(CORE_DIR)/obj

help:
	@sed -n '2,25p' Makefile

-include $(DEPS)
