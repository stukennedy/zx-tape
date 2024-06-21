# Generate ZX-Spectrum audio files from any file

## Installation

First clone this repo.

Then download the utility (zxtap-to-wav)[https://github.com/raydac/zxtap-to-wav]
(I downloaded one of the prebuilt releases and copied it in this folder)

Then get the utility (bas2tap[https://github.com/speccyorg/bas2tap]
This needs building from source:

```bash
gcc -Wall -O2 bas2tap.c -o bas2tap -lm ; strip bas2tap
```

## Run the app

```bash
python main.py example.js example
```
