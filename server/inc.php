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


function timerDiff($timeStart)
{
    return microtime(true) - $timeStart;
}
