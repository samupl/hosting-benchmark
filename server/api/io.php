<?php
header('Content-type: application/json');

include '../inc.php';
set_time_limit(60 * 2);

$results = array(
    "createAndRemoveEmpty" => array(),
    "smallWrite" => array(),
    "bigWrite" => array(),
    "randomWrite" => array(),
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
    $timeStart = microtime(true);
    for ($i = 0; $i < $count; $i++) {
        $file = fopen($path, 'w');
        fwrite($file, '');
        fclose($file);
        unlink($path);
    }
    $results["timeTaken"] = timerDiff($timeStart);
}

function testSmallWrite(&$results, $count = 99999) {
    $path = generateRandomFilePath();
    removeFileIfExists($path);
    $timeStart = microtime(true);
    $bytes = random_bytes($count);
    $file = fopen($path, 'w');
    for ($i = 0; $i < $count; $i++) {
        fwrite($file, $bytes[$i]);
    }
    fclose($file);
    unlink($path);
    $results["timeTaken"] = timerDiff($timeStart);
}

function testBigWrite(&$results, $count = 999) {
    $path = generateRandomFilePath();
    removeFileIfExists($path);
    $timeStart = microtime(true);
    $file = fopen($path, 'w');
    for ($i = 0; $i < $count; $i++) {
        fwrite($file, random_bytes(4096));
    }
    fclose($file);
    unlink($path);
    $results["timeTaken"] = timerDiff($timeStart);
}

function testRandomWrite(&$results, $count = 250, $multiplier = 250) {
    $filenames = array();
    for ($i = 0; $i < $count; $i++) {
        $filenames[] = generateRandomFilePath();
    }
    $timeStart = microtime(true);
    foreach ($filenames as $path) {
        $file = fopen($path, 'w');
        fwrite($file, '');
        fclose($file);
    }

    for ($i = 0; $i < $multiplier; $i++) {
        shuffle($filenames);
        foreach($filenames as $id => $path) {
            $file = fopen($path, 'a');
            fwrite($file, random_bytes(128));
            fclose($file);
        }
    }

    foreach($filenames as $id => $path) {
        unlink($path);
    }
    $results["timeTaken"] = timerDiff($timeStart);
}

testCreateAndRemove($results['createAndRemoveEmpty']);
testSmallWrite($results['smallWrite']);
testSmallWrite($results['bigWrite']);
testRandomWrite($results['randomWrite']);

echo json_encode($results);
