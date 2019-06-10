# Waze Travel Time Estimates

Integration with the (Waze)[https://www.waze.com/] route planner and navigation to automatically calculate
fastest time point to point which can be run on a job/schedule to estimate best travel times from multiple
locations. This is useful if you are relocating and want to find out topics such as "how long would it take
me to commute to work if I moved to location X".

## Dependency

This functionality is dependent on the following Python package - if this package changes or stops being
maintained, there is not guarantee that this functionality will work in the future:

[WazeRouteCalculator](https://github.com/kovacsbalu/WazeRouteCalculator)

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--waze-travel-time-estimates
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Configuration

Right now, there are hard-coded addresses in the script - this script/functionality has not yet been completed
to be more robust/usable, but serves as a decent starting point for exploring the Waze APIs.

## Usage

Simply execute the script:

```bash
$ python calc_travel_time.py
```

The output provided will contain a data structure with various fields to parse and will be enhanced in the future.
