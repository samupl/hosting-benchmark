<?php
header('Content-type: application/json');

include '../inc.php';
set_time_limit(60 * 2);

$results = array(
    "math" => array(),
    "string" => array(),
    "loops" => array(),
    "ifElse" => array(),
);

function testMath(&$results, $count = 99999) {
    $mathFunctions = array(
        "abs", "acos", "asin", "atan", "bindec", "floor", "exp", "sin", "tan",
        "pi", "is_finite", "is_nan", "sqrt",
    );
    $timeStart = microtime(true);
    for ($i = 0; $i < $count; $i++) {
        foreach ($mathFunctions as $function) {
            call_user_func_array($function, array($i));
        }
    }
    $results["timeTaken"] = timerDiff($timeStart);
}

function testString(&$results, $count = 99999)
{
    $stringFunctions = array(
        "addslashes", "chunk_split", "metaphone", "strip_tags", "md5", "sha1",
        "strtoupper", "strtolower", "strrev", "strlen", "soundex", "ord",
    );
    $string = 'the quick brown fox jumps over the lazy dog';
    $timeStart = microtime(true);
    for ($i = 0; $i < $count; $i++) {
        foreach ($stringFunctions as $function) {
            call_user_func_array($function, array($string));
        }
    }
    $results["timeTaken"] = timerDiff($timeStart);
}

function testLoops(&$results, $count = 999999)
{
    $timeStart = microtime(true);
    for ($i = 0; $i < $count; ++$i) {

    }

    $i = 0;
    while ($i < $count) {
        ++$i;
    }

    $results["timeTaken"] = timerDiff($timeStart);
}

function testIfElse(&$results, $count = 999999)
{
    $timeStart = microtime(true);
    for ($i = 0; $i < $count; $i++) {
        if ($i == -1) {

        } elseif ($i == -2) {

        } else {
            if ($i == -3) {

            }
        }
    }
    $results["timeTaken"] = timerDiff($timeStart);
}

testMath($results["math"]);
testString($results["string"]);
testLoops($results["loops"]);
testIfElse($results["ifElse"]);

echo json_encode($results);
