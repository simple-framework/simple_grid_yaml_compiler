import re
import urllib2
from urlparse import urlparse, urljoin


def generate_default_file_name(repo_info):
    return './.temp/' + repo_info['repo_name'] + '_defaults.yaml'


def generate_config_schema_file_name(repo_info):
    return './.temp/' + repo_info['repo_name'] + '_schema.yaml'


def generate_meta_info_file_name(repo_info):
    return './.temp/' + repo_info['repo_name'] + '_info.yaml'

def get_file_location(repo_info, file_type):
    base = "./.temp/" + repo_info["repo_name"]

    suffix = {
        "defaults": "_defaults.yaml",
        "config_schema": "_schema.yaml",
        "meta_info": "_info.yaml"
    }

    return base + suffix[file_type]

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

def get_repo_file(repo_url, file_name, file_type, post_func=None):
    try:
        base_url  = urlparse("https://raw.githubusercontent.com/")
        repo_info = analyse_repo_url(repo_url)

        repo_info_list = [
            repo_info['org_name'],
            repo_info['repo_name'],
            repo_info['branch_name'],
            file_name
        ]

        relative_url = urlparse('/'.join(x.strip() for x in repo_info_list))

        file_url = urljoin(base_url.geturl(), relative_url.geturl())

        response = urllib2.urlopen(file_url)

        file_loc = get_file_location(repo_info, file_type)

        with open(file_loc, "w") as file:
            file.write(response.read())

        if post_func is not None:
            return post_func(file_loc)

        return file_loc

    except Exception as ex:
        print(ex.message)


def get_meta_info(repo_url):
    return get_repo_file(repo_url, "meta-info.yaml", "meta_info", augment_meta_info)

def get_default_values(repo_url, default_file_name):
    return get_repo_file(repo_url, default_file_name, "defaults")

def get_config_schema(repo_url):
    return get_repo_file(repo_url, "config-schema.yaml", "config_schema")
