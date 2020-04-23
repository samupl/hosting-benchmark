<?php
header('Content-type: application/json');

$results = array(
    "phpVersion" => phpversion(),
    "platform" => PHP_OS,
);

echo json_encode($results);
