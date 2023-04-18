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
    $saveName = $_GET['name'];
    $databaseName = 'K-Means';
    $database = $connection->{$databaseName};
    $collectionName = 'K-Means Data';
    $collection = $database->{$collectionName};
    $query = ['saveName' => $saveName];
    $result = $collection->find($query);
    $docs = $result->toArray();
    if(!empty($docs))
    {
        $doc = current($docs);
        $rows = $doc['rows'];
        $cols = $doc['cols'];
        $clusters = $doc['clusters'];
        $originalName = $doc['originalName'];
        $status = $doc['status'];
        if($status == 'success')
        {
            echo "<h1>Success</h1><br>";
            echo "<h2>" . $originalName . " Info<h2><br>";
            echo "Rows:" . $rows . "<br>";
            echo "Cols:" . $cols . "<br>";
            echo "Clusters:" . $clusters . "<br>";

            echo "<a href='http://172.18.0.2/result/$saveName.txt' download='$saveName.txt'  ><h1>Download Result</h1></a>";	
            echo "<img src='http://172.18.0.2/result/$saveName.jpg' weidth='128' height='720' alt='result.jpg'><br>";
        }
        elseif($status === "congestion")
        {
            echo "<h1>Congestion</h1><br>";
            echo "<h2>" . $originalName . " Info<h2><br>";
            echo "Rows:" . $rows . "<br>";
            echo "Cols:" . $cols . "<br>";
            echo "Clusters:" . $clusters . "<br>";
            echo "<h1>Please wait</h1>";
        }
        else
        {
            echo "<h1>Error</h1><br>";
            echo "<h2>" . $originalName . " Info<h2><br>";
            echo "Rows:" . $rows . "<br>";
            echo "Cols:" . $cols . "<br>";
            echo "Clusters:" . $clusters . "<br>";
            echo "<a href='http://172.18.0.2/result/$saveName.log' download='$saveName.log'  ><h1>Error log</h1></a>";	
        }
    }
    else
    {
        echo "<h1>Unknow Error</h1>";
    }
?>