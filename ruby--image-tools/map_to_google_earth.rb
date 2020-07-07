require './lib/multi_logger'
require 'yaml'
require 'exifr'

# create a logger to output information
log_file     = File.open(File.join('logs', "#{Time.new.strftime('%Y%m%d_%k%M%S')}.log"), 'w')
logger       = Logger.new(MultiLogger.new(STDOUT, log_file))
logger.level = Logger::DEBUG

# load configurations for environment
CONFIG         = YAML.load_file('config/settings.yml')
source_dir     = CONFIG['image_source_dir']
kml_dir        = CONFIG['kml_destination_dir']
kml_filename   = "#{kml_dir}/#{Time.new.strftime("%Y%m%d_%k%M%S")}.kml"
data_point     = "A"
paths          = []
kml_data       = ''
point_data     = ''
animation_data = ''

# TODO: this should really be extracted into a templating language such as erb
# start to build the KML data
kml_data += <<-EOF
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
     xmlns:gx="http://www.google.com/kml/ext/2.2">
  <Document>
EOF

animation_data += <<-EOF
    <name>My Tour</name>
    <open>1</open>

    <gx:Tour>
      <name>Play</name>

      <gx:Playlist>
EOF

point_data += <<-EOF
  <Folder>
    <name>Points</name>

EOF

# some useful output
logger.info "================================= NEW RUN ======================================"
logger.info "Image Source Directory:    #{source_dir}"
logger.info "KML Destination Directory: #{kml_dir}"
logger.info "--------------------------------------------------------------------------------"
logger.info "Start Time:                  #{Time.new.strftime("%Y-%m-%d at %H:%M:%S")}"
logger.info "--------------------------------------------------------------------------------"

# parse each file in the source directory
Dir.foreach(source_dir) do |current_file|
  # ignore the current and upper directory items
  next if ['.', '..'].include?(current_file)

  # construct the fully qualified path
  current_file_qualified = File.join(source_dir, current_file)

  begin
    # attempt to obtain the required information
    exif_data = EXIFR::JPEG.new(current_file_qualified)
    gps_data  = exif_data.gps

    raise "No latitude/longitude data available" if gps_data.nil?

    # take the latitude/longitude and start building the XML
    coordinates = "#{gps_data.longitude},#{gps_data.latitude},#{gps_data.altitude}"
    paths       << coordinates

    # construct the animation data
    animation_data += <<-EOF
        <gx:FlyTo>
          <gx:duration>5.0</gx:duration>
          <Camera>
            <longitude>#{gps_data.longitude}</longitude>
            <latitude>#{gps_data.latitude}</latitude>
            <altitude>#{gps_data.altitude}</altitude>
            <heading>-6.333</heading>
            <tilt>33.5</tilt>
          </Camera>
        </gx:FlyTo>

        <gx:Wait>
          <gx:duration>1.0</gx:duration>
        </gx:Wait>

    EOF

    # construct the point data
    point_data += <<-EOF
    <Placemark>
      <name>#{data_point}</name>
      <description>
      </description>
      <Point>
        <coordinates>#{coordinates}</coordinates>
      </Point>
    </Placemark>
    EOF

    # increment the data point
    data_point.next!
  rescue Exception => error
    # fail-safe if the image EXIF data could not be retrieved
    logger.error "[FAIL] #{current_file} (#{error})"
    next
  end

  logger.debug "[SUCCESS] #{current_file} lat/lon retrieved"
end

# close out the points and animation section
point_data += <<-EOF
  </Folder>
EOF

animation_data += <<-EOF
    </gx:Playlist>
  </gx:Tour>
EOF

# add the animation and point data to the KML
kml_data << animation_data
kml_data << point_data

# add the paths to the KML
kml_data += <<-EOF
    <Placemark>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <coordinates>#{paths.join(' ')}</coordinates>
      </LineString>
    </Placemark>
EOF

# close out the KML
kml_data += <<-EOF
  </Document>
</kml>
EOF

# write the KML data to the file
File.open(kml_filename, 'w'){ |f| f.write kml_data }

# some useful output
logger.info "--------------------------------------------------------------------------------"
logger.info "End Time:                    #{Time.new.strftime("%Y-%m-%d at %H:%M:%S")}"
logger.info  "KML creation complete! You can find the KML file here: '#{kml_filename}'"
logger.info  "Open the KML file in Google Earth to see a map of your travels!"
logger.info "================================= END RUN ======================================"
