<?php
$twitter_id = “your_twitter_id”;

require ‘class/tmhOAuth/tmhOAuth.php’;
require ‘class/tmhOAuth/tmhUtilities.php’;

$tmhOAuth = new tmhOAuth(array(
'consumer_key' => '',
'consumer_secret' => '',
'user_token' => '',
'user_secret' => '',
));

$code = $tmhOAuth->request(‘GET’, $tmhOAuth->url(‘1.1/statuses/user_timeline’), array(
'screen_name' => $twitter_id,
'count' => '1'));

$response = $tmhOAuth->response[‘response’];
$twitFeed = json_decode($response, true);

foreach ($twitFeed as $latestFeed) {
$feedDate = $latestFeed[“created_at”];
$postedLast = explode(” “, $feedDate);
$feedCreatedAt = $postedLast[0].” - “.$postedLast[1].” “.$postedLast[2].”, “.$postedLast[5];
$feedMsg = $latestFeed[“text”];
$feedMsg = preg_replace(“/([\w]+\:\/\/[\w-?&;#~=.\/\@]+[\w\/])/”, “<a target="_blank" href="$1">$1</a>”, $feedMsg);
$feedMsg = preg_replace(“/#([A-Za-z0-9\/.]*)/”, “<a target="_new" href="http://twitter.com/search?q=$1">#$1</a>”, $feedMsg);
$feedMsg = preg_replace(“/@([A-Za-z0-9\/.]*)/”, “<a href="http://www.twitter.com/$1">@$1</a>”, $feedMsg);
}
?>


<a href=”https://twitter.com/<?php echo $twitter_id; ?>” target=”_blank”>@<?php echo $twitter_id; ?></a> <b>said:</b> <?php echo $feedMsg; ?> <b>last</b> <?php echo $feedCreatedAt; ?><br />