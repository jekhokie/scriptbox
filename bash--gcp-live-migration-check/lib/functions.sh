function get_live_migration_events () {
    write_output "Getting live migration events from system_event log..."

    if [ "$local_test" = true ]; then
        write_output "Running query locally"

        # query the local file for live migration events
        eventsTemp=$(cat $LOCAL_EVENTS)
    else
        write_output "Running query on user-configured GCP project"

        # get the provided date ranges, formatting the query dates appropriately
        if [ -z "${2}" ]; then
            dateRange="timestamp>=${1}"
        else
            dateRange="timestamp>=${1} AND timestamp<=${2}"
        fi

        # perform a stackdriver query for event logs
        read -r -d '' logQuery <<EOF
            logName=projects/${GCP_PROJECT}/logs/cloudaudit.googleapis.com%2Fsystem_event AND
            resource.type="gce_instance" AND
            operation.producer="compute.instances.migrateOnHostMaintenance" AND
            ${dateRange}
EOF
        eventsTemp=$(gcloud logging read "$logQuery" --project=${GCP_PROJECT} --format="json(timestamp,protoPayload.resourceName)")
    fi

    # parse query results (if any)
    migrationEvents=($(echo $eventsTemp | jq -r '.[] | "\(.timestamp)|\(.protoPayload.resourceName)"'))
}

function print_current_day_migration_results {
    write_output "Parsing list of migrations..."
    echo "| --------------------------------------------------------------------------------------------------------------------------------------------------------------- |"
    printf "| %-30s | %-30s | %-93s |\n" "GMT" "LOCAL" "RESOURCE"
    echo "| ------------------------------ | ------------------------------ | --------------------------------------------------------------------------------------------- |"
    for migration in "${migrationEvents[@]}"; do
        gmtDate=${migration%|*}
        gmtEpochSec="$(date -ujf "%FT%T" ${gmtDate} +'%s' 2>/dev/null)"
        localDate=$(TZ=$DESIRED_TZ date -jf "%s" $gmtEpochSec)
        printf "| %-30s | %-30s | %-93s |\n" "${gmtDate}" "${localDate}" "${migration##*|}"
    done
    echo "| --------------------------------------------------------------------------------------------------------------------------------------------------------------- |"
}

function print_migration_trends {
    write_output "Parsing list of migrations..."
    echo "| ----------------------------------------------------- |"
    printf "| %-30s | %-20s |\n" "DATE RANGE" "# MIGRATIONS"
    echo "| ------------------------------ | -------------------- |"
    for migration in "${migrationTrends[@]}"; do
        dateRange=$(echo "${migration% *}" | sed -e 's/\\n/ -> /')
        printf "| %-30s | %-20s |\n" "${dateRange}" "${migration##* }"
    done
    echo "| ----------------------------------------------------- |"
}

function graph_migration_trends {
    write_output "Graphing trends..."
    read -r -d '' GNUPLOT_SCRIPT <<EOF
    set nokey;
    set yrange [0:];
    set ytic 50;
    set terminal dumb 170,40;
    set title 'GCP Live Migrations';
    set xlabel 'Week';
    set lmargin screen 0.08;
    set ylabel 'Migrations' offset character -3,0;
    set boxwidth 0.5;
    set tics nomirror;
    plot '-' using 2:xtic(1) with boxes;
EOF
    echo "${trendsDB}" | gnuplot -persist -e "${GNUPLOT_SCRIPT}"
}
