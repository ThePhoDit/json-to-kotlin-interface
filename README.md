# Get a Kotlin interface from a JSON file

usage: tmp.py [-h] -f FILE [-o OUTPUT]

Convert JSON to Kotlin interface

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  JSON file path.
  -o OUTPUT, --output OUTPUT (optional, defaults to `Interface.kt`)
                        Kotlin file path where contents should be dumped. If the file exists it overrides its contents
