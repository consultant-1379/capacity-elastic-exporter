#!/bin/bash

# Make sure expected arguments were provided
if [ $# -lt 3 ]; then
    echo "Invalid number of arguments!"
    echo "This script is used to clean time based indices from Elasticsearch. The indices must have a"
    echo "trailing date in a format that can be represented by the UNIX date command such as '%Y-%m-%d'."
    echo ""
    echo "Usage: `basename $0` host_url index_prefix num_days_to_keep [date_format]"
    echo "The date_format argument is optional and defaults to '%Y-%m-%d'"
    echo "Example: `basename $0` http://localhost:9200 cflogs- 7"
    echo "Example: `basename $0` http://localhost:9200 elasticsearch_metrics- 31 %Y.%m.%d"
    exit
fi

elasticsearchUrl=$1
indexNamePrefix=$2
numDaysDataToKeep=$3
dateFormat=%Y-%m-%d
if [ $# -ge 4 ]; then
    dateFormat=$4
fi

# Get the curent date in a 'seconds since epoch' format
curDateInSecondsSinceEpoch=$(date +%s)
#echo "curDateInSecondsSinceEpoch=$curDateInSecondsSinceEpoch"

# Subtract numDaysDataToKeep from current epoch value to get the last day to keep
let "targetDateInSecondsSinceEpoch=$curDateInSecondsSinceEpoch - ($numDaysDataToKeep * 86400)"
#echo "targetDateInSecondsSinceEpoch=$targetDateInSecondsSinceEpoch"

while : ; do
    # Subtract one day from the target date epoch
   let "targetDateInSecondsSinceEpoch=$targetDateInSecondsSinceEpoch - 86400"
   #echo "targetDateInSecondsSinceEpoch=$targetDateInSecondsSinceEpoch"

   # Convert targetDateInSecondsSinceEpoch into a YYYY-MM-DD format
   targetDateString=$(date --date="@$targetDateInSecondsSinceEpoch" +$dateFormat)
   #echo "targetDateString=$targetDateString"

   # Format the index name using the prefix and the calculated date string
   #indexName="$indexNamePrefix$targetDateString"
   indexName="$targetDateString$indexNamePrefix"
   #echo "indexName=$indexName"

   # First check if an index with this date pattern exists
    # Curl options:
    #  -s   silent mode. Don't show progress meter or error messages
    #  -w "%{http_code}\n" Causes curl to display the HTTP status code only after a completed transfer.
    #  -I Fetch the HTTP-header only in the response. For HEAD commands there is no body so this keeps curl from waiting on it.
    #  -o /dev/null Prevents the output in the response from being displayed. This does not apply to the -w output though.
   httpCode=$(curl -o /dev/null -s -w "%{http_code}\n" -I -X HEAD "$elasticsearchUrl/$indexName")
   #echo "httpCode=$httpCode"
   if [ $httpCode -ne 200 ]
   then
      echo "Index $indexName does not exist. Stopping processing."
      break;
   fi

   # Send the command to Elasticsearch to delete the index. Save the HTTP return code in a variable
   httpCode=$(curl -o /dev/null -s -w "%{http_code}\n" -X DELETE $elasticsearchUrl/$indexName)
   #echo "httpCode=$httpCode"

   if [ $httpCode -eq 200 ]
   then
      echo "Successfully deleted index $indexName."
    else
      echo "FAILURE! Delete command failed with return code $httpCode. Continuing processing with next day."
      continue;
   fi

   # Verify the index no longer exists. Should return 404 when the index isn't found.
   httpCode=$(curl -o /dev/null -s -w "%{http_code}\n" -I -X HEAD "$elasticsearchUrl/$indexName")
   #echo "httpCode=$httpCode"
   if [ $httpCode -eq 200 ]
   then
      echo "FAILURE! Delete command responded successfully, but index still exists. Continuing processing with next day."
      continue;
   fi

done

