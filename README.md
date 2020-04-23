# hosting-benchmark

A full web-hosting benchmark suite

## Installation

Install using pip:

```shell script
pip install hosting-benchmark
```

## Usage

The benchmark consists of two components:

* A *server*, which is a set of PHP scripts that run the benchmark
* A *client*, which is a cli (command line interface) tool used to run the 
  benchmark and collect/present the data.
  
In order to run the benchmark, you need to install the server app. This is 
fairly straightforward:

* Create a MySQL database on your web hosting, note down the credentials
* Run `hosting-benchmark archive` to prepare a ZIP archive with the server.
  You will be asked to provide your database credentials
* Upload and extract the zip package to your web hosting http root directory
* Run the benchmark using:

```shell script
hosting-benchmark --hostname=https://example.com/ --count=10 --sleep=5 all
```

To learn what the `--count` and `--sleep` flags do, please invoke
`hosting-benchmark --help`.
