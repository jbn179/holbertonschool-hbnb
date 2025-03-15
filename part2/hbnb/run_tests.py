import unittest
import sys
import os

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to sys.path
sys.path.append(current_dir)

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    
    # Use the absolute path to the tests directory
    tests_dir = os.path.join(current_dir, 'tests', 'test_models')
    test_suite = test_loader.discover(tests_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
