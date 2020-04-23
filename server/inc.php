<?php

if (!@include 'config.php')
  die('Please create the config.php file. Refer to README for more details.');


function dieConfigError($msg) {
  die("Config error: $msg");
}

function validateConfig() {
  if (empty($GLOBALS['dbuser']))
    die('Config error: $dbuser is empty.');

  if (empty($GLOBALS['dbpass']))
    die('Config error: $dbpass is empty.');

  if (empty($GLOBALS['dbhost']))
    die('Config error: $dbhost is empty.');

  if (empty($GLOBALS['dbname']))
    die('Config error: $dbname is empty.');
}

validateConfig();


function timerDiff($timeStart) {
    return microtime(true) - $timeStart;
}


function uuid4() {
    $data = openssl_random_pseudo_bytes(16);
    assert(strlen($data) == 16);

    $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
    $data[8] = chr(ord($data[8]) & 0x3f | 0x80);

    return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}
