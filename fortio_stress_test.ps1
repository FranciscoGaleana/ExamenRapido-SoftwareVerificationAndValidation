#Relative paths
$fortioPath = ".\fortio.exe"
$inputFile = "requests.jsonl"
$outputDirectory = "fortio_results"

#File to track progress of of stress testing
$logProgress = "log_progress.txt"
Set-Content $logFile "" 

#Create output directories if they don't exist
if (!(Test-Path $outputDirectory)) { 
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null 
}


#Configuration options for fortio
$options = @(
    "load",         #Indicates that a load test will be carried out
    "-c", "1",      #1 concurrent connection
    "-qps", "0",    #0 indicates that there is no request limit per second, thus they will be send as fast as possible
    "-uniform",     #Generate requests uniformly
    "-nocatchup",   #Evitar acumulación de solicitudes
    "-n", "1"       #Total amount of requests per endpoint that will be send
)

$counter = 1
#Read requests line by line (iterating each line of the jsonl)
Get-Content $inputFile -ReadCount 1 | ForEach-Object {
    $request = $_ | ConvertFrom-Json    #For each line, it will convert the JSON into an object
    $method = $request.method.ToUpper() #Retrieving request type
    $url = $request.url                 #Retrieving endpoint URL
    $payload = $request.payload         #Retrieving payload for POST requests

    #Build output file name per endpoint (3 different endpoints, thus 3 different files)
    $cleanUrl = $url.Replace("http://", "").Replace("/", "_").Replace(":", "_")
    $outputFile = Join-Path $outputDirectory ("results_" + $method + "_" + $cleanUrl + ".json")

    Write-Host "`nStarting test #$counter : $method $url"

    #Build base command 
    $cmd = $Options + @("-json", $outputFile)

    #If request type is POST
    if ($method -eq "POST") {
        $rawPayload = $payload | ConvertTo-Json -Compress

        $cmd += @("-X", "POST", "-H", "Content-Type: application/json", "--payload", $rawpayload, $url)
    }

    #If request type is GET
    elseif ($method -eq "GET") {
        $cmd += $url
    }

    #In case there is an unsopported request type (not GET or POST)
    else {
        Write-Warning "Unsupported HTTP method: $method"
        continue
    }

    #Execute Fortio
    & $fortioPath $cmd

    Write-Host "Test #$counter finished - output saved in: $outputFile"
    $counter++

    # Log progress every 50,000 tests
    if ($counter % 5000 -eq 0) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "$timestamp - Completed $counter tests" | Out-File -FilePath $logProgress -Append
    }
}

Write-Host "`nAll $($counter - 1) tests completed. Results in '$outputDirectory'"
