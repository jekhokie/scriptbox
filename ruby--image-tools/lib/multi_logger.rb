# class to allow logging to multiple destinations
# such as STDOUT and a log file
class MultiLogger
  def initialize(*destinations)
    @destinations = destinations
  end

  def write(*args)
    @destinations.each do |log|
      log.write(*args)
    end
  end

  def close
    @destinations.each do |destination|
      destination.close
    end
  end
end
