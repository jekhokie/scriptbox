import java.util.Calendar;
import java.util.TimeZone;
import org.rrd4j.core.*;
import org.rrd4j.ConsolFun;

class RRD4JReader {
    /***************** CONFIGURATION *****************/
    public static final String RRD_FILENAME = "activeThreads.rrd";
    public static final int    LAST_SECONDS = 10;
    /*****************   ENDCONFIG   *****************/

    // entry point
    public static void main(String[] args) {
        // calculate start/end times based on desired "last x seconds" configuration
        long endTime = Calendar.getInstance().getTimeInMillis() / 1000;
        long startTime = endTime - LAST_SECONDS;

        try {
            // read the rrd file and capture data
            RrdDb rrd = new RrdDb("rrds/" + RRD_FILENAME);
            FetchRequest fetchRequest = rrd.createFetchRequest(ConsolFun.AVERAGE, startTime, endTime);
            FetchData fetchData = fetchRequest.fetchData();
            rrd.close();

            // output some meta information
            System.out.println("Start Time: " + startTime);
            System.out.println("End Time: " + endTime);
            System.out.println("Rows: " + fetchData.getRowCount());
            System.out.println("Cols: " + fetchData.getColumnCount());
            System.out.println("Step: " + fetchData.getStep() + "s");
            System.out.println("Data Points:");

            // obtain timestamps and corresponding values
            long[] times = fetchData.getTimestamps();
            double[] vals = fetchData.getValues("activeThreads");

            // output the results
            for (int i = 0; i < times.length; i++) {
                System.out.println(times[i] + " - " + vals[i]);
            }
        } catch (Exception e) {
            System.out.println("Error - something bad happened: " + e.getMessage());
        }
    }
}
