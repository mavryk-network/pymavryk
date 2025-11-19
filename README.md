# PyMavryk

[![Twitter](https://badgen.net/badge/icon/MavrykDynamics?icon=twitter&label=)](https://twitter.com/MavrykDynamics)
[![Monthly downloads](https://static.pepy.tech/badge/pymavryk/month)](https://pepy.tech/project/pymavryk)
[![GitHub stars](https://img.shields.io/github/stars/mavryk-network/pymavryk?color=2c2c2c&style=plain)](https://github.com/mavryk-network/pymavryk)
[![Python Version](https://img.shields.io/pypi/pyversions/pymavryk?color=2c2c2c)](https://www.python.org)
<br>
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mavryk-network/pymavryk/master?filepath=michelson_quickstart.ipynb)
[![License: MIT](https://img.shields.io/github/license/mavryk-network/pymavryk?color=2c2c2c)](https://github.com/mavryk-network/pymavryk/blob/next/LICENSE)
[![Latest release](https://img.shields.io/github/v/release/mavryk-network/pymavryk?label=version&color=2c2c2c)](https://github.com/mavryk-network/pymavryk/releases)
[![GitHub issues](https://img.shields.io/github/issues/mavryk-network/pymavryk?color=2c2c2c)](https://github.com/mavryk-network/pymavryk/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/mavryk-network/pymavryk?color=2c2c2c)](https://github.com/mavryk-network/pymavryk/pulls)

* RPC query engine
* Cryptography
* Building and parsing operations
* Smart contract interaction
* Local forging/packing & vice versa
* Working with Michelson AST

#### PyMavryk CLI
* Generating contract parameter/storage schema
* Activating and revealing accounts
* Deploying contracts (+ GitHub integration)

#### Michelson REPL

* Builtin interpreter (reimplemented)
* Set of extra helpers (stack visualization, blockchain context mocking)

#### Michelson Jupyter kernel

* Custom interpreter with runtime type checker
* Syntax highlighting, autocomplete with `Tab`
* In-place docstrings with `Shift+Tab`
* Macros support
* Verbose execution logging
* Debug helpers

#### Michelson integration testing framework

* Writing integration tests using `unittest` package
* Simulating contract execution using remote intepreter (via RPC) or builtin one

## Installation

Make sure you have Python 3.8 to 3.12 installed and set as default in the system.  

You also need to install cryptographic packages before installing the library/building the project:

### Linux

#### Ubuntu, Debian and other apt-based distributions

```shell
$ sudo apt install libsodium-dev libgmp-dev pkg-config
```

#### Arch Linux

```shell
$ sudo pacman -Syu --needed libsodium gmp
```

### MacOS

[Homebrew](https://brew.sh/) needs to be installed.

```shell
$ brew install libsodium gmp pkg-config
```

#### M1 (ARM)

In case `libsodium` or `gmp` cannot find either include or lib paths, try explicitly set environment vars:

```shell
export CFLAGS="-I/opt/homebrew/Cellar/gmp/6.2.1_1/include/ -L/opt/homebrew/Cellar/gmp/6.2.1_1/lib/"
export DYLD_LIBRARY_PATH=/opt/homebrew/lib/
pip3 install --user pymavryk
```

For running tests you might also need to export `LD_LIBRARY_PATH`:

```shell
export LD_LIBRARY_PATH=/opt/homebrew/lib/
```

### Windows

The recommended way is to use WSL and then follow the instructions for Linux,
but if you feel lucky you can try to install natively:

1. Install MinGW from [https://osdn.net/projects/mingw/](https://osdn.net/projects/mingw/)
2. Make sure `C:\MinGW\bin` is added to your `PATH`
3. Download the latest libsodium-X.Y.Z-msvc.zip from [https://download.libsodium.org/libsodium/releases/](https://download.libsodium.org/libsodium/releases/).
4. Extract the Win64/Release/v143/dynamic/libsodium.dll from the zip file
5. Copy libsodium.dll to C:\Windows\System32\libsodium.dll

### From PyPi

```shell
$ pip install wheel setuptools pkginfo cryptography
$ pip install pymavryk
```

### [Google Colab](https://colab.research.google.com)

`````python
>>> !apt install libsodium-dev libgmp-dev
>>> !pip install pymavryk
`````

### Docker container

Verified & minified images for CI/CD https://hub.docker.com/r/mavrykdynamics/pymavryk/tags

```shell
$ # 1. Use image from registry
$ docker pull mavrykdynamics/pymavryk
$ # or build it yourself
$ docker build . -t pymavryk
$ # 2. Use included docker-compose.yml
$ docker-compose up -d notebook
```

### Building from sources

Requirements:

* Python 3.8 to 3.12
* libsodium, coincurve, gmp
* make

```shell
$ # prepare environment
$ make install
# # run full CI with tests
$ make all
```

## Quick start

Read [quick start guide](https://pymavryk.mavryk.org/quick_start.html)  
Learn how to [enable Jupyter with Michelson](./src/michelson_kernel/README.md)

## API reference

Check out a complete [API reference](https://pymavryk.mavryk.org/contents.html)

### Inline documentation

If you are working in Jupyter/Google Colab or any other interactive console, you can display documentation for a particular class/method:

```python
>>> from pymavryk import pymavryk
>>> pymavryk
```

### Contact

* Telegram chat: [@MavrykNetwork](https://t.me/MavrykNetwork)

## Credits

* **This project is a fork of [PyTezos](https://github.com/baking-bad/pytezos) by [Baking Bad](https://baking-bad.org/), licensed under the MIT License**
* The original PyTezos project was initially started by Arthur Breitman, and is now maintained by the Baking Bad team
* Baking Bad is supported by Tezos Foundation
* Michelson test set from the Mavryk repo is used to ensure the interpreter workability
* Michelson structured documentation by Nomadic Labs is used for inline help
