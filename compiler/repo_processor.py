import re
import urllib2
from urlparse import urlparse, urljoin


def generate_file_name(repo_info, file):
    return {
        "meta-info.yaml": './.temp/' + repo_info['repo_name'] + '_info.yaml',
        "config-schema.yaml": './.temp/' + repo_info['repo_name'] + '_schema.yaml',
        "site_level_configuration_defaults.yaml": './.temp/' + repo_info['repo_name'] + '_defaults.yaml',
        "default-data.yaml": './.temp/' + repo_info['repo_name'] + '_defaults.yaml'
    }[file]

def analyse_repo_url(repo_url):
    repo_analysis = re.search('//.*/(.*)/(.*)', repo_url)
    org_name = repo_analysis.group(1)
    repo_name = repo_analysis.group(2)
    ##TODO fetch branch info
    branch = 'master'
    return {
        'org_name':org_name,
        'repo_name': repo_name,
        'branch_name': branch
    }

def generate_meta_info_parent_name(meta_info_file):
    with open(meta_info_file, 'r') as meta_info:
        for line in meta_info:
            if "component" in line:
                parent_name = line.split(':')[1].strip().lower()
                return 'meta_info_' + ''.join(parent_name.split('"'))

def augment_meta_info(meta_info_file):
    augmented_meta_info = ""
    component_line = ""
    meta_info_parent_name = generate_meta_info_parent_name(meta_info_file)
    with open(meta_info_file, 'r') as meta_info:
        for line in meta_info:
            augmented_meta_info += "    " + line
    augmented_meta_info = meta_info_parent_name + ":\n" + augmented_meta_info
    with open(meta_info_file, 'w') as meta_info:
        meta_info.write(augmented_meta_info)
        return meta_info

def get_repository_file(repo_url, file, is_meta_file=False):
    try:
        base_url = urlparse("https://raw.githubusercontent.com/")
        repo_info = analyse_repo_url(repo_url)
        repo_info_list = [repo_info['org_name'], repo_info['repo_name'], repo_info['branch_name'], file]
        relative_url = urlparse("/".join(x.strip() for x in repo_info_list))
        meta_info_url = urljoin(base_url.geturl(), relative_url.geturl())
        response = urllib2.urlopen(meta_info_url)
        meta_info = response.read()
        fname = generate_file_name(repo_info, file)
        with open(fname, 'w') as f:
            f.write(meta_info)
            f.close()
        if is_meta_file:
            return augment_meta_info(fname)
        return fname
    except Exception as ex:
        print ex.message