<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>BIND Query Log</title>
  </head>
  <body>
    <div class="container">
      <h1 class="text-center mt-2">Latest BIND Query Logs (Last 10)</h1>
      <hr class="mt-1 mb-1"/>
      <p class="text-center"><strong>NOTE:</strong> Queries are shown in reverse order (newest first/at the top of the table).</p>

      <div class="row">
        <div class="col text-center">
          <a role="button" class="text-center btn btn-primary btn-sm mb-3" href="index.php">REFRESH</a>
        </div>
      </div>

      <table class="table table-striped table-sm table-bordered">
        <thead>
          <tr>
            <th scope="col">Query Record</th>
            <th scope="col">Requested At</th>
            <th scope="col">Requestor</th>
          </tr>
        </thead>
        <tbody>
          <?php
            $NUM_RESULTS = 5;

            $data = file_get_contents('/bind9-logs/bind.log');
            $queryMatches = array();

            if(preg_match_all("/^.*queries.*\$/m", $data, $queryMatches)){
              $i = 0;
              foreach (array_reverse($queryMatches[0]) as $match) {
                $queryRecord = "UNKNOWN";
                $requestedAt = "UNKNOWN";
                $requestor = "UNKNOWN";

                // parse requestor
                $regExp = "/.*0[xX][0-9a-fA-F]+ (.*)#.*/";
                $requestorMatches = array();
                if (preg_match($regExp, $match, $requestorMatches) ) {
                  $requestor = $requestorMatches[1];
                }

                // parse date
                $regExp = "/^(.*) queries.*/";
                $dateMatches = array();
                if (preg_match($regExp, $match, $dateMatches) ) {
                  $requestedAt = $dateMatches[1];
                }

                // parse query record
                $regExp = "/.* query: (.*) IN .*/";
                $queryMatches = array();
                if (preg_match($regExp, $match, $queryMatches) ) {
                  $queryRecord = $queryMatches[1];
                }

                echo "<tr>";
                echo "  <td>" . $queryRecord . "</td>";
                echo "  <td>" . $requestedAt . "</td>";
                echo "  <td>" . $requestor . "</td>";
                echo "</tr>";

                $i += 1;
                if ($i >= $NUM_RESULTS) {
                  break;
                }
              }
            }
            else{
             echo "<p>No queries found</p>";
            }
          ?>
        </tbody>
      </table>

      <h1 class="text-center mt-2">Latest OpenLDAP Query Logs (Last 10)</h1>
      <hr class="mt-1 mb-1"/>
      <p class="text-center"><strong>NOTE:</strong> Queries are shown in reverse order (newest first/at the top of the table).</p>

      <table class="table table-striped table-sm table-bordered">
        <thead>
          <tr>
            <th scope="col">Query Record</th>
            <th scope="col">Requested At</th>
          </tr>
        </thead>
        <tbody>
          <?php
            $data = file_get_contents('/openldap-logs/openldap.log');
            $queryMatches = array();

            if(preg_match_all("/^.*SRCH.*\$/m", $data, $queryMatches)){
              $i = 0;
              foreach (array_reverse($queryMatches[0]) as $match) {
                $queryRecord = "UNKNOWN";
                $requestedAt = "UNKNOWN";

                // parse date
                $regExp = "/^(.*) openldap-service.*/";
                $dateMatches = array();
                if (preg_match($regExp, $match, $dateMatches) ) {
                  $requestedAt = $dateMatches[1];
                }

                // parse query record
                $regExp = "/.* SRCH (.*) scope.*/";
                $queryMatches = array();
                if (preg_match($regExp, $match, $queryMatches) ) {
                  $queryRecord = $queryMatches[1];
                }

                echo "<tr>";
                echo "  <td>" . $queryRecord . "</td>";
                echo "  <td>" . $requestedAt . "</td>";
                echo "</tr>";

                $i += 1;
                if ($i >= $NUM_RESULTS) {
                  break;
                }
              }
            }
            else{
             echo "<p>No queries found</p>";
            }
          ?>
        </tbody>
      </table>

      <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </div>
  </body>
</html>
