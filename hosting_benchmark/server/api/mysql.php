<?php
header('Content-type: application/json');

include '../inc.php';
include '../fake_data.php';
include '../LoremIpsum.php';

set_time_limit(60 * 2);

function getMysqliObject() {
    $mysqli = new mysqli($GLOBALS['dbhost'], $GLOBALS['dbuser'], $GLOBALS['dbpass'], $GLOBALS['dbname']);
    if ($mysqli->connect_error) {
        die('Could not connect to database');
    }
    return $mysqli;
}

$results = array(
    "insert" => array(),
    "insertSingleTransaction" => array(),
);

function createSchema() {
    $queries = array(
        "DROP TABLE IF EXISTS questions;",
        "DROP TABLE IF EXISTS users;",
        "DROP TABLE IF EXISTS answers;",
        "DROP TABLE IF EXISTS comments;",
        "CREATE TABLE users (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(128) NOT NULL,
            email VARCHAR(256) NOT NULL,
            reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=INNODB;",
        "CREATE TABLE questions (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            author_id INT UNSIGNED,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX i_author_id (author_id),
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE RESTRICT,
            title VARCHAR(128) NOT NULL,
            content TEXT NOT NULL
        ) ENGINE=INNODB;"
    );

    $mysqli = getMysqliObject();
    foreach($queries as $query) {
        $result = $mysqli->query($query);
        if (!$result) die('Failed to execute query: '.$query);
    }
    $mysqli->close();
}


function createRandomUser($mysqli) {
    $firstName = $GLOBALS['firstName'];
    $lastName = $GLOBALS['lastName'];
    $freeEmailDomain = $GLOBALS['freeEmailDomain'];
    $username = $firstName[array_rand($firstName)].''.$lastName[array_rand($lastName)];
    $email = $firstName[array_rand($firstName)].''.$lastName[array_rand($lastName)].'@'.$freeEmailDomain[array_rand($freeEmailDomain)];
    $query = "INSERT INTO users (username, email) VALUES (?, ?)";
    $stmt = $mysqli->prepare($query);
    $stmt->bind_param("ss", $username, $email);
    $result = $stmt->execute();

    if (!$result) die('Failed to insert user: '.$query);
}

function createRandomQuestion($stmt, $userId) {
    $lipsum = new joshtronic\LoremIpsum();
    $title = $lipsum->words(10);
    $content = $lipsum->sentences(10);
    $stmt->bind_param("iss", $userId, $title, $content);
    $result = $stmt->execute();
    if (!$result) die('Failed to insert question: '.$query);
}

function testInsert(&$results) {
    $timeStart = microtime(true);
    for ($i = 0; $i < 10000; $i++) {
        $mysqli = getMysqliObject();
        createRandomUser($mysqli);
        $mysqli->close();
    }
    $results["timeTaken"] = timerDiff($timeStart);
}

function testinsertSingleTransaction(&$results, $count = 20000) {
    $timeStart = microtime(true);
    $mysqli = getMysqliObject();
    $mysqli->begin_transaction();
    for ($i = 0; $i < $count; $i++) {
        $query = "INSERT INTO questions (author_id, title, content) VALUES (?, ?, ?)";
        $stmt = $mysqli->prepare($query);
        createRandomQuestion($stmt, rand(1, 10000));
    }
    $mysqli->commit();
    $mysqli->close();
    $results["timeTaken"] = timerDiff($timeStart);
}


createSchema();

// The insert tests are also populating the database with random data.
testInsert($results['insert']);
testinsertSingleTransaction($results['insertSingleTransaction']);

echo json_encode($results);
