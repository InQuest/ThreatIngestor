"""
This script validates your YAML syntax and checks that you have the minimum required (`config.yml`) by ThreatIngestor to operate properly.
"""

import sys, yaml

from shutil import which
from subprocess import getoutput
from rich.console import Console

try:
    config_file = sys.argv[1]
except IndexError:
   print("Missing config.yml file location")
   print("Usage: python3 scripts/validate.py config.yml")
   sys.exit(1)

def validate_config():
    if which("yamllint") is not None:
        lint = getoutput(f"yamllint {config_file}")

        if "error" in lint:
            # If you get get a line-length error, add this line to the yaml config on the same line: '# yamllint disable-line'
            print(f"\nYaml config errors:\n{lint}")
            return False
        elif "warning" in lint:
            if "-v" in sys.argv:
                print(f"\nYaml config warnings:\n{lint}")

        return True
    else:
        print("Missing yamllint")
        sys.exit(1)

def main():
    if validate_config():
        console = Console()

        with console.status("[bold green]Validating config", spinner="aesthetic"):
            with open(config_file) as f:
                yaml_file = yaml.safe_load(f)

                try:
                    console.log(f"[green]Validating sources...[/green]")

                    for source in yaml_file['sources']:

                        # Slow down the output
                        if "-v" in sys.argv:
                            from time import sleep
                            sleep(0.2)

                        try:
                            console.log(f"[green]Validating[/green] {source['name']}")
                        except KeyError:
                            console.log(f"[red]Validation Failed[/red] {source}")
                            console.log(f"Missing the 'name' key for {source}")
                            continue

                        try:
                            source_module = source['module']

                            if "rss" in source_module:
                                try:
                                    _ = source['feed_type']
                                except KeyError:
                                    console.log(f"[red]Validation Failed[/red] {source}")
                                    console.log(f"Missing the 'feed_type' key for one or more of your rss modules")
                                    continue

                        except KeyError:
                            console.log(f"[red]Validation Failed[/red] {source}")
                            console.log(f"Missing the 'module' key for one or more of your sources")
                            continue
                except KeyError:
                    console.log(f"'sources' is required. Refer to the ThreatIngestor documentation here: https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources.html")
                    sys.exit(1)

                try:
                    console.log(f"[green]Validating operators...[/green]")

                    for operator in yaml_file['operators']:
                        try:
                            console.log(f"[green]Validating[/green] {operator['name']}")
                        except KeyError:
                            console.log(f"[red]Validation Failed[/red] {operator}")
                            console.log(f"Missing the 'name' key for {operator}")
                            continue

                        try:
                            _ = operator['module']
                        except KeyError:
                            console.log(f"[[red]Validation Failed[/red]] {operator}")
                            console.log(f"Missing the 'module' key for one or more of your operators")
                            continue

                        try:
                            _ = operator['filename']
                        except KeyError:

                            if operator['module'] not in ["threatkb", "sqs", "mysql"]:
                                console.log(f"[[red]Validation Failed[/red]] {operator}")
                                console.log(f"Missing the 'filename' key for one or more of your operators")
                                continue
                            else:
                                pass
                except KeyError:
                    console.log(f"[red]Validation Failed[/red] 'operators' is required. Refer to the ThreatIngestor documentation here: https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators.html")
                    sys.exit(1)

if __name__ == '__main__':
    main()
