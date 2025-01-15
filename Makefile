export PROJECT ?= $(shell basename $(shell pwd))
TRONADOR_AUTO_INIT := true

GITVERSION ?= $(INSTALL_PATH)/gitversion
GH ?= $(INSTALL_PATH)/gh
YQ ?= $(INSTALL_PATH)/yq
TOML ?= toml

-include $(shell curl -sSL -o .tronador "https://cowk.io/acc"; echo .tronador)

## Node Version Bump and creates VERSION File - Uses always the FullSemVer from GitVersion (no need to prepend the 'v').
version: packages/install/gitversion
	$(call assert-set,GITVERSION)
ifeq ($(GIT_IS_TAG),1)
	@echo "$(GIT_TAG)" | sed -e 's/^v\([0-9]\{1,\}\.[0-9]\{1,\}\.[0-9]\{1,\}\(-[a-zA-Z0-9.]\{1,\}\)*\)\(+deploy-.*\)\?$$/\1/' > VERSION
	@$(TOML) set --toml-path pyproject.toml project.version "$$(cat VERSION)"
else
	# Translates + in version to - for helm/docker compatibility
	@echo "$(shell $(GITVERSION) -output json -showvariable FullSemVer | tr '+' '-')" > VERSION
	@$(TOML) set --toml-path pyproject.toml project.version "$(shell $(GITVERSION) -output json -showvariable FullSemVer | tr '+' '-')"
endif

code/install/tomlcli:
	@pip3 install toml-cli

# Modify package.json to change the project name with the $(PROJECT) variable
## Code Initialization for Node Project
code/init: packages/install/gitversion packages/install/gh packages/install/yq code/install/tomlcli
	$(call assert-set,GITVERSION)
	$(call assert-set,GH)
	$(call assert-set,YQ)
	$(eval $@_OWNER := $(shell $(GH) repo view --json 'name,owner' -q '.owner.login'))
	@$(TOML) set --toml-path pyproject.toml project.name "$(PROJECT)"
	@$(TOML) set --toml-path pyproject.toml project.version "$(shell $(GITVERSION) -output json -showvariable MajorMinorPatch | tr '+' '-')"
