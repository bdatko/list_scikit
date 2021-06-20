## 0.1.0 (2021-06-19)

### Feat

- **pyproject.toml**: add versioning to project
- **figure.py**: refactor the cli into a seperate module so make can cache results
- **post.py**: add cli to create md of the post
- **makefile**: add the target of md file for the post
- **post.py**: add cli for craete the venn diagram
- **makefile**: add venn diagram target
- **makefile**: add target for scikit-learn related libraries list
- **post.py**: add post.py script
- **list_scikit/__init__.py-list_scikit/constants.py**: add constants module to package
- **all**: initial git

### Refactor

- **makefile**: seperate out targets into seperate modules file
- **post.py**: refactor out prepare and figure into seperate modules so make can cache results
- **prepare.py**: refactor preprocessing of the raw text data into a seperate module so make can cache results

### Fix

- **pyproject.toml**: change python version to allow for pandas library
