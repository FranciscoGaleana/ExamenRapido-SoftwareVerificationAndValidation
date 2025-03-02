#Relative path to fortio executable
$fortioPath = ".\fortio.exe"

#Configuration options for fortio
$options = @(
    "load",         #Indicates that a load test will be carried out
    "-c", "1",      #1 concurrent connection
    "-qps", "0"     #0 indicates that there is no request limit per second, thus they will be send as fast as possible
    "-uniform",     #Generate requests uniformly
    "-nocatchup",   #Evitar acumulación de solicitudes
    "-n", "1"       #Total amount of requests per endpoint that will be send
)

#API Endpoints
$endpoints = @(
    @{"method" = "GET"; "url" = "http://127.0.0.1:5000/business/info"},
    @{"method" = "GET"; "url" = "http://127.0.0.1:5000/business/products"},
    @{"method" = "POST"; "url" = "http://127.0.0.1:5000/business/products"; "payload" = '{\"ProductName\": \"Microphone\"}'},
    @{"method" = "POST"; "url" = "http://127.0.0.1:5000/business/products"; "payload" = '{\"Product\": \"Mousepad\"}'},
    @{"method" = "GET"; "url" = "http://127.0.0.1:5000/business/contact";}
)

$counter = 1
#Iterating over each endpoint to execute the test
foreach($endpoint in $endpoints){
    
    Write-Host "`nStarting test: $counter-------------------"
    #If type request is POST
    if($endpoint.method -eq "POST") {
        & $fortioPath $options -X POST -H "Content-Type: application/json" --payload "$($endpoint.payload)" "$($endpoint.url)"
    }

    #If type request is GET
    elseif ($endpoint.method -eq "GET") {
        & $fortioPath $options "$($endpoint.url)"

    }
    
    Write-Host "Test: $counter finished-------------------"
    Write-Host "-----------------------------------`n"
    $counter++
}

Write-Host "Tests completed"