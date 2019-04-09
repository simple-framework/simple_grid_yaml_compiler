from compiler.repo_processor import analyse_repo_url, generate_file_name, augment_meta_info, generate_meta_info_parent_name, get_repository_file

from os import mkdir, remove
from shutil import rmtree
from urllib2 import urlopen

import unittest

class RepoProcessorTest(unittest.TestCase):
	def test_analyse_repo_url(self):
		repo_url = "https://github.com/WLCG-Lightweight-Sites/simple_grid_yaml_compiler"
		
		expected_output = {
			"org_name": "WLCG-Lightweight-Sites",
			"repo_name": "simple_grid_yaml_compiler",
			"branch_name": "master"
		}

		self.assertDictEqual(analyse_repo_url(repo_url), expected_output)

	def test_generate_default_file_name(self):
		repo_info = {
			"org_name": "WLCG-Lightweight-Sites",
			"repo_name": "simple_grid_yaml_compiler",
			"branch_name": "master"
		}

		expected_output = "./.temp/simple_grid_yaml_compiler_defaults.yaml"

		self.assertEqual(generate_file_name(repo_info, "site_level_configuration_defaults.yaml"), expected_output)

	def test_generate_config_schema_file_name(self):
		repo_info = {
			"org_name": "WLCG-Lightweight-Sites",
			"repo_name": "simple_grid_yaml_compiler",
			"branch_name": "master"
		}

		expected_output = "./.temp/simple_grid_yaml_compiler_schema.yaml"

		self.assertEqual(generate_file_name(repo_info, "config-schema.yaml"), expected_output)

	def test_generate_meta_info_file_name(self):
		repo_info = {
			"org_name": "WLCG-Lightweight-Sites",
			"repo_name": "simple_grid_yaml_compiler",
			"branch_name": "master"
		}

		expected_output = "./.temp/simple_grid_yaml_compiler_info.yaml"

		self.assertEqual(generate_file_name(repo_info, "meta-info.yaml"), expected_output)

	def test_get_default_values(self):
		repo_url      = "https://github.com/WLCG-Lightweight-Sites/simple_grid_site_defaults"
		defaults_file = "site_level_configuration_defaults.yaml"

		fname  = get_repository_file(repo_url, defaults_file)

		with open(fname, "r") as file:
			output = file.read()

		file_url        = "https://raw.githubusercontent.com/WLCG-Lightweight-Sites/simple_grid_site_defaults/master/site_level_configuration_defaults.yaml"
		expected_output = urlopen(file_url).read()

		self.assertEqual(output, expected_output)

	def test_get_config_schema(self):
		repo_url = "https://github.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream"

		get_repository_file(repo_url, "config-schema.yaml")

		repo_info = analyse_repo_url(repo_url)
		fname     = generate_file_name(repo_info, "config-schema.yaml")

		with open(fname, "r") as file:
			output = file.read()

		file_url = "https://raw.githubusercontent.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream/master/config-schema.yaml"
		expected_output = urlopen(file_url).read()

		self.assertEqual(output, expected_output)

	def test_get_meta_info(self):
		repo_url = "https://github.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream"

		get_repository_file(repo_url, "meta-info.yaml",True)

		repo_info = analyse_repo_url(repo_url)
		fname     = generate_file_name(repo_info, "meta-info.yaml")

		with open(fname, "r") as file:
			output = file.read()

		file_name = "meta_info.expected"

		file_url = "https://raw.githubusercontent.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream/master/meta-info.yaml"
		meta_info_output = urlopen(file_url).read()

		with open(file_name, "w") as file:
			file.write(meta_info_output)

		augment_meta_info(file_name)

		with open(file_name, "r") as file:
			expected_output = file.read()

		self.assertEqual(output, expected_output)

	def test_augment_meta_info(self):
		base_fname     = "./tests/data/meta_info.yaml"
		test_fname     = "./.temp/meta_info.yaml"
		expected_fname = "./tests/data/augmented_meta_info.yaml"

		with open(base_fname, "r") as base, open(test_fname, "w") as test:
			test.write(base.read())

		augment_meta_info(test_fname)

		with open(test_fname, "r") as test, open(expected_fname, "r") as expected:
			self.assertEqual(test.read(), expected.read())

		remove(test_fname)

	def test_generate_meta_info_parent_name(self):
		fname = "./tests/data/meta_info.yaml"

		expected_output = "meta_info_test"

		self.assertEqual(generate_meta_info_parent_name(fname), expected_output)
