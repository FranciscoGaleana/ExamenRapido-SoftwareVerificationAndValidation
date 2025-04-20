#Number of requests
$totalRequests = 1000000

#Output file
$outputFile = "requests.jsonl"

#Clear existing file or create it
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}
New-Item -Path $outputFile -ItemType File -Force | Out-Null

$stream = [System.IO.StreamWriter]::new($outputFile, $false)

try {
    $getUrls = @(
        "http://127.0.0.1:5000/business/info",
        "http://127.0.0.1:5000/business/products",
        "http://127.0.0.1:5000/business/contact"
    )

    $knownProduct = "Product-1"
    #Creating 1,000,0000 requests
    for($i = 1; $i -le $totalRequests; $i++){
        #Each even iteration, a POST request will be sended
        if ($i % 2 -eq 0){
            $url = "http://127.0.0.1:5000/business/products"
            $rand = Get-Random -Minimum 1 -Maximum 100

            #80% chance of inserting valid data
            if($rand -le 80){
                $productName = "Product-$i"
                $payload = '{"ProductName": "' + $productName + '"}'
            }

            #10% chance of inserting duplicates
            elseif ($rand -le 90){
                $payload = '{"ProductName": "' + $knownProduct + '"}'
            }

            #10% chance of inserting data with invalid key name
            else {
                $payload = '{"product": "InvalidKeyName"}'
            }

            $entry = @{ method = "POST"; url = $url; payload = $payload} | ConvertTo-Json -Compress
        }

        #Each uneven iteration, a GET request will be sended to a random endpoint
        else {
            $entry = @{ method = "GET"; url = Get-Random -InputObject $getUrls;} | ConvertTo-Json -Compress
        }

        $stream.WriteLine($entry)
    }

    Write-Host "Done writing $totalRequests requests to $outputFile"

} finally {
    $stream.Close()
}
