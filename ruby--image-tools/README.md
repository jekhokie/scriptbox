# Image Tools

This project is a collection of scripts that allow various image transformation options. Each
script that is provided is explained in detail below the setup instructions.

## Setup

The following setup instructions pertain to the project as a whole - once the below configurations
and dependencies have been addressed, you will be able to use any of the scripts provided in this
repository.

### Dependencies

This project requires the following:

- Ruby
- Bundler

### Configuration

- Clone the repository

- Install the required dependencies

```bash
$ bundle install
```

- Copy the sample configuration file and edit it for your environment:

```bash
$ cp config/settings.yml.sample config/settings.yml
$ vim config/settings.yml
# using vim or the editor of your choice, edit the file for your environment
```

## Capabilities

### Sort By EXIF Date

Script Name: sort_by_date_time.rb

This script provides a way to copy image files to a directory with filenames corresponding to
the *original* created date/time based on EXIF data, resulting in a date/time sorted order of
the images.

#### Background

Many times (on a vacation or otherwise) photographs are taken using multiple devices,
such as iPhones, DSLR cameras, iPods, etc. When downloading all of these images to
a computer and putting them into a directory to show others/organize, these files are
typically downloaded with various names and 'created at' date/times based on the local
file system. This makes it very difficult to sort through the pictures and determine the
overall sequence of events.

The EXIF data for the photographs (different from the file system data based on when the image
was copied to the file system) still maintains the *original* created date/time. This script
utilizes the EXIF created date/time to copy all photographs to a target directory and name the
files based on the EXIF created date/time. This allows weaving the photographs from various
devices into a single, date/time series sequence, allowing the user to view all photographs in
the exect order they were taken, regardless of which device they originated from.

#### Usage

To use the script, simply execute it using Ruby:

```bash
$ bundle exec ruby sort_by_date_time.rb
```

Once the process completes, it will inform you of the location that contains the images with
updated filenames (which allows sorting by date/time).

### Map to Google Earth

Script Name: map_to_google_earth.rb

This script takes a directory of images and generates a Google Earth KML file. This file can be
used to map a time-series path of where pictures were taken if the pictures contain latitude and
longitude (as well as time) data in the EXIF data.

#### Background

After returning from a vacation, it is sometimes interesting to think of where you traveled.
Typically, you have a range of pictures that you've taken at various places. Using these pictures,
it is possible to map the time-series path that was taken on the vacation to give an idea of
where you traveled. Obviously this is entirely dependent on the latitude/longitude and time data
being accurate in the EXIF data of the pictures, but if the data is present, it is possible to
re-create the time-series path of travel based on the pictures provided.

Photographs contained in a directory can be utilized to create a Google Earth KML file, which
allows you to view your travels within Google Earth based on the data extracted from the photos
using this script capability.

#### Usage

To use the script, simply execute it using Ruby:

```bash
$ bundle exec ruby map_to_google_earth.rb
```

Following completion of this script, it will inform you of where the Google Earth KML file is
located. Using this file, you can view your travels on a Google Earth application.

## Troubleshooting

All logs are both output to the terminal when run and stored in a log file with a date/time
filename under the logs/ directory. Please inspect the logs for any issues/errors that may occur.
