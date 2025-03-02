<?php
if ($argc != 2) {
	echo "Usage: php script.php n\n";
	exit(1);
}
$n = (int)$argv[1];
for ($i = 0; $i < $n; $i++) {
	// mt_rand returns an integer, so we divide by mt_getrandmax() to get a float in [0,1]
	echo (mt_rand() / mt_getrandmax()) . " ";
}
echo "\n";
