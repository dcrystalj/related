<?php
ini_set('error_reporting', E_ALL);
require 'rb.php';

R::setup('mysql:host=localhost;dbname=wordpress', 'root','root');

$blog = $_GET['blog'];

$r = R::findOne('reccommend', 'link = ? AND blog = ?',[$_GET['link'], $blog]);

if (isset($_GET['json']) && $_GET['json'] == "true") { //more for debug
    print $r->posts;
} else {
    $posts = json_decode($r->posts, true);

    print "<ul>";

    foreach ($posts as $post) {
        $p = R::findOne('reccommend', 'post_id = ? and blog = ?', [$post, $blog]);
        print '<li><a target="_parent" href="'. $p->link . '">' . $p->title . '</a></li>';
    }

    print "</ul>";
}

?>
