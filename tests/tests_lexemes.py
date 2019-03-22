from compiler.lexemes import get_repo_list, parse_for_variable_hierarchies
from ruamel.yaml.comments import CommentedSeq, CommentedMap
import unittest


class TestLexemes(unittest.TestCase):
    def test_get_repo_list(self):
        input = open('./tests/data/lexemes_test', "r")
        self.assertEqual(get_repo_list(input), ["https://github.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream"])

    def test_parse_for_variable_hierarchies(self):
        data = 'testStr'
        keyword = 'Key'
        self.assertEqual(data, parse_for_variable_hierarchies(data, keyword))

        data = CommentedSeq()
        data.insert(0, 'First')
        data.insert(1, 'Second')
        data.insert(2, 'Third')
        data.insert(3, 'Key')
        self.assertEqual('Key', parse_for_variable_hierarchies(data, keyword))

        data = CommentedMap()
        data.insert(0, 'First', 'test1')
        data.insert(1, 'Second', 'test2')
        data.insert(2, 'Third', 'test3')
        data.insert(3, 'Key', 'test4')
        self.assertEqual('test4', parse_for_variable_hierarchies(data, keyword))


if __name__ == '__main__':
    unittest.main()
