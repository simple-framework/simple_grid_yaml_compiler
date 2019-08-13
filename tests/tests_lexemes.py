import unittest

class MyTest(unittest.TestCase):
    def test(self):
        input = """
        lightweight_components:
  - type: compute_element
    repository_url: "https://github.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream"
    nodes:
      - node: lw-site-droplet-0
        container_count: 1
      - node: ec2-18-184-37-92.eu-central-1
        container_count: 2
    preferred_tech_stack:
      level_2_configuration: yaim
      """    

        #self.assertEqual(input, ["https://github.com/WLCG-Lightweight-Sites/wlcg_lightweight_site_ce_cream"])