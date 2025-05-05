<?php
if (!isset($_GET['query'])) {
    echo "No query received.";
    exit;
}

$query = urlencode($_GET['query']);
$apiKey = 'YOUR_BING_API_KEY'; // ?? Replace this with your actual key
$endpoint = "https://api.bing.microsoft.com/v7.0/search?q=$query";

// Set up the HTTP request
$headers = [
    "Ocp-Apim-Subscription-Key: $apiKey"
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $endpoint);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

$response = curl_exec($ch);
$http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_status != 200) {
    echo "<p>Error contacting Bing API. HTTP Status: $http_status</p>";
    exit;
}

$data = json_decode($response, true);

echo "<h2>Results for: " . htmlspecialchars($_GET['query']) . "</h2>";

if (isset($data['webPages']['value'])) {
    echo "<ul>";
    foreach ($data['webPages']['value'] as $result) {
        $title = htmlspecialchars($result['name']);
        $url = htmlspecialchars($result['url']);
        $snippet = htmlspecialchars($result['snippet']);
        
        echo "<li><a href='$url' target='_blank'><strong>$title</strong></a><br>$snippet</li><br>";
    }
    echo "</ul>";
} else {
    echo "<p>No results found.</p>";
}
?>
