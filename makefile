SHELL=/usr/bin/bash
.DEFAULT_GOAL := help

env_name:=list_scikit
conda:=conda
fixtures:=tests/fixtures/
pytestflags:=

conda_root := /c/Users/benda/miniconda3/Scripts
conda_activate := $(conda_root)/activate
activate_env := source $(conda_activate) $(env_name)

.PHONY: all
## Make the project
all: .cenv data/scikit_related_projects.rst data/libraries.csv data/venn.png scikit_learn_related_post.md

## Create the environment.yaml file from poetry2conda
environment.yaml: pyproject.toml
	poetry2conda --dev pyproject.toml environment.yaml

## Create the conda environment from the `environment.yml` you have to activate afterwards
.cenv: environment.yaml
	$(conda) env create --quiet --force --file environment.yaml; \
	touch .cenv
	@echo to activate: conda activate $(env_name)

## Get the scikit-learn list
data/scikit_related_projects.rst:
	curl -o $@ https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/related_projects.rst

## Create the list of libraries from scikit-learn related projects
data/libraries.csv: post.py data/scikit_related_projects.rst
	$(activate_env) && python $< create_scikit_offical data/scikit_related_projects.rst $@

## Create the Venn digram comparing scikit-learn with my own list
data/venn.png: post.py data/libraries.csv list_scikit/constants.py
	$(activate_env) && python $< create_venn_figure data/libraries.csv data/venn.png

## Create the markdown post
scikit_learn_related_post.md: post.py data/libraries.csv data/venn.png list_scikit/constants.py
	$(activate_env) && python $< create_post data/libraries.csv scikit_learn_related_post.md

.PHONY: test
## Test for source and activate
test:
	@echo $(activate_env) && python --version 


.PHONY: realclean
## Remove unused conda packages then remove the environment
realclean:
	$(conda) clean -a
	$(conda) env remove --name $(env_name)
	rm -f .cenv

# Adopted from https://gist.github.com/klmr/575726c7e05d8780505a
# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) == Darwin && echo '--no-init --raw-control-chars')
