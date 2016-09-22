# RRD4j Reader

Java application that can read an RRD4J-generated RRD file and output results.

## Warning

I fully realize that the setup of this project is a no-no from a Java perspective (compiled jars,
no use of Maven, etc.). This project is not an attempt to meet Java standards and guidelines - it is
intended to provide a quick implementation to demonstrate how to read/parse RRD4J-generated RRDs.

## Java Prerequisites

The application in this project has been built and tested with Java 1.7 - if using a different Java
version, your mileage may vary.

## Configuration

Prior to compiling, there are a couple configuration items in the RRD4JReader.java file. Inspect the
section titled "CONFIGURATION" (near the top of the class definition) and set the configurations for
your needs. You may not need to adjust anything and the application should work with the provided
defaults given that there is a sample RRD file in the rrds/ directory.

## Compile

To compile the test application, perform the following:

```bash
$ javac -cp "lib/rrd4j-3.0.jar:." -d build/ RRD4JReader.java
# will compile and place the Java class file in the build/ directory
```

## Usage

Once the Java application has been compiled, you can run it to retrieve the last X seconds of data
(as defined in the CONFIGURATION section of the class definition) via the following:

```bash
java -cp "lib/rrd4j-3.0.jar:." RRD4JReader
# should output data like the following:
#   Start Time: 1474565534
#   End Time: 1474565544
#   Rows: 2
#   Cols: 1
#   Step: 60s
#   Data Points:
#   1474565520 - 1.2452523652e+02
#   1474565580 - 5.1234321523e+02
```

Note that if the data output reflects a lot of `NaN` values, it is likely because the RRD sample
file does not have data close enough to the current day/time you are running the application and
you might try including a different RRD file in the `rrds/` directory and re-configuring the
`RRD_FILENAME` variable/re-compiling for your needs.
