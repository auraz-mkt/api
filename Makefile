################################################################################
##                                 ENVIRONMENT                                ##
################################################################################

# Include environment variables from .env
include .env

################################################################################
##                                   COMMANDS                                 ##
################################################################################

MAKE += --no-print-directory RECURSIVE=1

ifndef VERBOSE
DOCKER := docker --log-level "info"
DOCKER_IMAGE := $(DOCKER) image
COMPOSE := $(DOCKER) compose 2>/dev/null
COMPOSE_BUILD := $(COMPOSE) build -q
HEROKU := heroku
else
DOCKER := docker --log-level "error"
DOCKER_IMAGE := $(DOCKER) image
COMPOSE := $(DOCKER) compose
COMPOSE_BUILD := $(COMPOSE) build
HEROKU := heroku
endif

################################################################################
##                                    COLORS                                  ##
################################################################################

RES := \033[0m
MSG := \033[1;36m
ERR := \033[1;31m
SUC := \033[1;32m
WRN := \033[1;33m

################################################################################
##                                  AUXILIARY                                 ##
################################################################################

# Variable do allow is-empty and not-empty to work with ifdef/ifndef
export T := 1

define is-empty
$(strip $(if $(strip $1),,T))
endef

define not-empty
$(strip $(if $(strip $1),T))
endef

define message
printf "${MSG}%s${RES}\n" $(strip $1)
endef

define success
(printf "${SUC}%s${RES}\n" $(strip $1); exit 0)
endef

define warn
(printf "${WRN}%s${RES}\n" $(strip $1); exit 0)
endef

define failure
(printf "${ERR}%s${RES}\n" $(strip $1); exit 1)
endef

define compare
cat $(strip $1) | diff - $(strip $2)
endef

################################################################################
##                                   BUILD                                    ##
################################################################################

build:
	@$(call message,"Building ${MODE} API image with label ${LABEL}")
	@env API_VERSION=${LABEL} $(COMPOSE_BUILD) api --build-arg API_MODE=${MODE}

build-dev:
	@$(MAKE) build MODE="development" LABEL="dev"

build-prod:
	@$(MAKE) build MODE="production" LABEL="latest"

release:
	@$(call message,"Releasing API version ${TAG}")
	@$(DOCKER_IMAGE) tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:${TAG}
	@$(DOCKER_IMAGE) push ${DOCKER_IMAGE}:${TAG}

heroku-deploy:
	@$(call message,"Deploying API image to Heroku registry")
	@$(HEROKU) container:push web --app auraz-api
	@$(call success,"API image deployed to Heroku registry")

heroku-release:
	@$(call message,"Releasing latest API at Heroku")
	@$(HEROKU) container:release web --app auraz-api
	@$(call success,"Latest API released at Heroku")

################################################################################
##                                    RUN                                     ##
################################################################################

start:
	@$(COMPOSE) up api

stop:
	@$(COMPOSE) down api

restart:
	@$(COMPOSE) restart api
