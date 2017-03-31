<?php

// configuration
$url = 'index.php';
$filename = time() . '.webedit.csv';
$file = '/home/pi/ap/www/recordings/' . $filename;
//print $file;

// check if form has been submitted
if (isset($_POST['text']))
{
    // save the text contents
    file_put_contents($file, $_POST['text']);

    // redirect to form again
    header(sprintf('Location: %s', $url));
    printf('<a href="%s">Moved</a>.', htmlspecialchars($url));
    exit();
}

// read the latest recording

$files = glob('recordings/*.csv') ;
//print_r( $files);
asort ($files);

//print_r($files);

//print array_pop($files); 

$text = file_get_contents(array_pop($files));


?>
<a href="/recordings/">Previous recordings to download</a>
<br />

Edit the latest recording (saves to new file):
<!-- HTML form -->
<form action="" method="post"  >
<textarea name="text" rows=40 cols=100><?php echo htmlspecialchars($text) ?></textarea>
<input type="submit" />
<input type="reset" />
</form>