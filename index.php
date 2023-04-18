<html>
	<title>K-means Calculate </title>
	<head>
		<h1>K-Means Calculate</h1>
	</head>
	<body>
        <form method="post" action="upload.php" enctype="multipart/form-data">
        Please Upload The File(.xlsx)<input required type="file" id="fileUpload" accept=".xlsx" name="fileUpload"/>
        <br>
        Rows:<input autocomplete="off" required type="text" name="rows" />
        <br>
        Columns:<input autocomplete="off" required type="text" name="cols" />
        <br>
        Target Clusters:<input autocomplete="off" required type="text" name="clusters" />
        <br>
        <button id="upload_button" type="submit">
            Upload And Execute
        </button>
        </form>
	</body>
</html>
