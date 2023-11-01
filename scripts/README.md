# ThreatIngestor Utilities

Scripts to improve ThreatIngestor usage and help with minimizing errors.

All scripts contain the following optional argument to allow for higher verbosity in stdout:

```bash
python3 scripts/<script> -v
```

A quick list of all available scripts:

| Script                | Example                           | Description                                                                                                                                |
|-----------------------|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `scripts/validate.py` | `python3 validate.py config.yml`  | This script validates your YAML syntax and checks that you have the minimum required (`config.yml`) by ThreatIngestor to operate properly. |
| `scripts/build.sh`    | `chmod +x build.sh && ./build.sh` | Basic script to build a fresh installation of ThreatIngestor locally.                                                                      |
