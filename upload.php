<?php
    require 'vendor/autoload.php';
    $connection = new MongoDB\Client("mongodb://172.18.0.3:27017/");
    try
    {
        $connection->listDatabases();
    }
    catch(MongoDB\Driver\Exception\ConnectionException $ex)
    {
        echo "<h1>Database connect fail</h1><br>";
        echo $ex->getMessage();
    }
    $rows = $_POST['rows'];
    $cols = $_POST['cols'];
    $clusters = $_POST['clusters'];
    $originalName = $_FILES["fileUpload"]["name"];
    $savePath = "/var/www/html/data/";
    $saveName = md5($_FILES["fileUpload"]["tmp_name"]);
    if(move_uploaded_file($_FILES["fileUpload"]["tmp_name"], $savePath . $saveName . ".xlsx"))
    {
        $database = $connection->selectDatabase("K-Means");
        $collection = $database->selectCollection("K-Means Data");
        $collection->insertOne([
            'originalName' => $originalName,
            'saveName' => $saveName,
            'rows' => $rows,
            'cols' => $cols,
            'clusters' => $clusters,
            'status' => 'congestion'
        ]);
        header("Location: http://172.18.0.2/display.php?name=" . $saveName);
        exit();
    }
    else
    {
        echo "<h1>Upload fail</h1>";
    }
?>
<input type ="button" onclick ="javascript:location.href='http://172.18.0.2/index.php'" value="Go to home"></input>