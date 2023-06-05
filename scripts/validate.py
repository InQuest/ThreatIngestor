import sys, yaml

from shutil import which
from subprocess import getoutput

config_file = sys.argv[1]
verbose = sys.argv

def verbose_mode():
    if "v" in verbose:
        verbosity = True
    else:
        verbosity = False

    return verbosity

def validate_config():
    if which("yamllint") is not None:

        if verbose_mode():
            lint = getoutput(f"yamllint {config_file}")
        else:
            lint = getoutput(f"yamllint {config_file} --no-warnings")

        if "error" in lint:
            print(f"\nYaml config errors:\n{lint}")
            return False
        else:
            if verbose_mode() and lint:
                print(f"\nYaml config warnings:\n{lint}")
            
            return True
    else:
        print("Missing yamllint")
        sys.exit(1)

def main():
    if validate_config():
        with open(config_file) as f:
            yaml_file = yaml.safe_load(f)

            for sources in yaml_file['sources']:
                try:
                    _ = sources['name'],  sources['module']

                    if "rss" in sources['module']:
                        try:
                            _ = sources['feed_type']
                        except KeyError:
                            print(f"\nValidation failed. Location: {sources}")
                            print(f"Missing the `feed_type` key for one or more of your rss module(s).")
                            continue

                    if verbose_mode():
                        print(f"Name: {sources['name']}, Module: {sources['module']}")
                except KeyError:
                    print(f"\nValidation failed. Location: {sources}")
                    print(f"Missing the `module` key for one or more of your sources.")
                    continue

            for operators in yaml_file['operators']:
                try:
                    _ = operators['name'], operators['module']

                    if verbose_mode():
                        print(f"Name: {operators['name']}, Module: {operators['module']}")
                except KeyError:
                    print(f"\nValidation failed. Location: {operators}")
                    print(f"Missing the `module` key for one or more of your operators.")
                    continue

if __name__ == '__main__':
    main()