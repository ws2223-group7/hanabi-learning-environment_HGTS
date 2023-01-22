pylint $(git ls-files '*.py' ':!:hanabi_learning_environment/*' ':!:examples/*')
/bin/python3 -m unittest
