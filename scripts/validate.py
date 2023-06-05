import sys, yaml

from shutil import which
from subprocess import getoutput

config_file = sys.argv[1]
verbose = sys.argv

def is_command_available(exe):
    return which(exe) is not None

def verbose_mode():
    if "v" in verbose:
        verbosity = True
    else:
        verbosity = False

    return verbosity

def validate_config():
    if is_command_available("yamllint"):

        if verbose_mode():
            lint = getoutput(f"yamllint {config_file}")
        else:
            lint = getoutput(f"yamllint {config_file} --no-warnings")

        if "error" in lint:
            print(f"\nYaml config errors:\n{lint}")
            return False
        else:
            if verbose_mode():
                print(f"\nYaml config warnings:\n{lint}")
            
            return True
    else:
        print("Missing yamllint")
        sys.exit(1)

def main():
    if validate_config():
        with open(config_file) as f:
            yaml_file = yaml.safe_load(f)

            for _ in yaml_file:

                try:
                    sources = yaml_file['sources'][0]
                    data = f"[Source] Name: {sources['name']}, Module: {sources['module']}"

                    if verbose_mode():
                        print(data)
                except KeyError:
                    print(f"[Source] Validation failed. Error: {sources}")
                    sys.exit(1)
                
                try:
                    operators = yaml_file['operators'][0]
                    data = f"[Operator] Name: {operators['name']}, Module: {operators['module']}"

                    if verbose_mode():
                        print(data)
                except KeyError:
                    print(f"[Operator] Validation failed. Error: {operators}")
                    sys.exit(1)

        print("\nValidation complete. Looks good.\n")

if __name__ == '__main__':
    main()