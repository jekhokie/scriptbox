require './lib/multi_logger'
require 'yaml'
require 'exifr'

# create a logger to output information
log_file     = File.open(File.join('logs', "#{Time.new.strftime('%Y%m%d_%k%M%S')}.log"), 'w')
logger       = Logger.new(MultiLogger.new(STDOUT, log_file))
logger.level = Logger::DEBUG

# load configurations for environment
CONFIG     = YAML.load_file('config/settings.yml')
source_dir = CONFIG['image_source_dir']
dest_dir   = CONFIG['image_destination_dir']

# some useful output
logger.info "================================= NEW RUN ======================================"
logger.info "Image Source Directory:      #{source_dir}"
logger.info "Image Destination Directory: #{dest_dir}"
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
    # attempt to construct the target filename
    created_date          = EXIFR::JPEG.new(current_file_qualified).date_time
    target_file           = created_date.strftime("%Y%m%d_%k%M%S.jpg")
    target_file_qualified = File.join(dest_dir, target_file)

    # copy the file to the target
    FileUtils.cp current_file_qualified, target_file_qualified
  rescue Exception => error
    # fail-safe if the image EXIF data could not be retrieved
    logger.error "[FAIL] #{current_file} (#{error})"
    next
  end

  logger.debug "[SUCCESS] #{current_file} --> #{target_file}"
end

# some useful output
logger.info "--------------------------------------------------------------------------------"
logger.info "End Time:                    #{Time.new.strftime("%Y-%m-%d at %H:%M:%S")}"
logger.info  "Conversion complete! Please have a look in '#{dest_dir}' for date/time sequenced images!"
logger.info "================================= END RUN ======================================"
