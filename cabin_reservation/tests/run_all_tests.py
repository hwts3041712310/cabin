# run_all_tests.py

import unittest

loader = unittest.TestLoader()
suite = loader.discover(start_dir='.', pattern='test_*.py')

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)