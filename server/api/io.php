<?php
header('Content-type: application/json');

include '../inc.php';
set_time_limit(60 * 2);

$results = array(
    "createAndRemoveEmpty" => array(),
    "smallWrite" => array(),
);


function generateRandomFilePath() {
    $filename = 'test_'.uuid4();
    return 'tmp/'.$filename;
}

if (!is_dir('tmp/')) {
    mkdir('tmp', 0755, true);
}

function removeFileIfExists($path) {
    if (file_exists($path))
        unlink($path);
}

function testCreateAndRemove(&$results, $count = 5000) {
    $path = generateRandomFilePath();
    removeFileIfExists($path);
    $bytes = random_bytes($count);
    $timeStart = microtime(true);
    for ($i = 0; $i < $count; $i++) {
        $file = fopen($path, 'w');
        fwrite($file, $bytes[$i]);
        fclose($file);
        unlink($path);
    }
    $results["timeTaken"] = timerDiff($timeStart);
}

function testSmallWrite(&$results, $count = 99999) {
    $path = generateRandomFilePath();
    removeFileIfExists($path);
    $timeStart = microtime(true);
    $file = fopen($path, 'w');
    for ($i = 0; $i < $count; $i++) {
        fwrite($file, 'a');
    }
    fclose($file);
    unlink($path);
    $results["timeTaken"] = timerDiff($timeStart);
}

testCreateAndRemove($results['createAndRemoveEmpty']);
testSmallWrite($results['smallWrite']);

echo json_encode($results);
