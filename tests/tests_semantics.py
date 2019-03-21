from compiler.semantics import check_yaml_syntax
import unittest
from yamllint.config import YamlLintConfig
from yamllint import linter

class MyTest(unittest.TestCase):
  conf = YamlLintConfig('extends: relaxed')

  def test_check_yaml_syntax(self):   
    augmented_yaml_file = check_yaml_syntax('../.temp/runtime.yaml')
    file = open(augmented_yaml_file)
    gen = linter.run(file,self.conf)
    errors = list(gen)
    self.assertEqual(errors,[])

if __name__ == '__main__':
    unittest.main()
