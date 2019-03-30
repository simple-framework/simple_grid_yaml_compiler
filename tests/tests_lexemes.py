from compiler.lexemes import get_repo_list, parse_for_variable_hierarchies
from ruamel.yaml.comments import CommentedSeq, CommentedMap
import unittest

class Test_get_repo_list(unittest.TestCase):
    def test(self):
        
        with open("./tests/resources/complete_config.yaml", "r") as f:
            self.assertEqual(
                    get_repo_list(f), 
                    [
                        "https://github.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream",
                        "https://github.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_wn_pbs"
                    ])

class Test_parse_for_variable_hierarchies(unittest.TestCase):

    def test_data_type_neither_CommentedSeq_nor_CommentedMap(self):

        data = dict({})
        self.assertEqual(data, parse_for_variable_hierarchies(data, "__from__"))
    

    def test_datatype_is_CommentedSeq(self):

        c = CommentedSeq()
        c.insert(0, "key")
        c.insert(1, "to")
        
        c2 = CommentedMap()
        c2.insert(0, "to", "from")
        c2.insert(1, "__from__", "to")

        c.insert(2, c2)

        result = CommentedSeq()
        result.append("key")
        result.append("to")
        result.append("to")

        self.assertEqual(result, parse_for_variable_hierarchies(c, "__from__"))


    def test_datatype_is_CommentedMap(self):

        c = CommentedMap()
        c.insert(0, "key", "value")
        c.insert(1, "__from__", "test")

        self.assertEqual("test", parse_for_variable_hierarchies(c, "__from__"))

        c1 = CommentedMap()
        c1.insert(0, "key", "value")

        c2 = CommentedMap()
        c2.insert(0, "to", "from")
        c2.insert(1, "__from__", "to")

        c1.insert(2, "someseq", c2)

        result = CommentedMap()
        result.insert(0, "key", "value")
        result.insert(1, "someseq", "to")

        self.assertEqual(result, parse_for_variable_hierarchies(c1, "__from__"))

