<html>
<body>

<?php

$myFile = "/tmp/request.log";
$fh = fopen($myFile, 'a');

$user = $_GET["user"];
$pass = $_GET["pass"];
$choice = $_GET["drop"];
$amount = $_GET["amount"];

$mysqli = new mysqli('localhost', 'root', 'rootmysql', 'ctf2');
if (!$mysqli) 
{
   die('Could not connect: ' . $mysqli->error());
}
$url="process.php?user=$user&pass=$pass&drop=balance";
if ($choice == 'register')
{
   $query = "insert into users (user,pass) values ('$user', '$pass')";
   $result = $mysqli->query($query);
   die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
}
else if ($choice == 'balance')
{
   $query = "select * from transfers where user='$user'";
   $result = $mysqli->query($query);
   $sum = 0;
   print "<H1>Balance and transfer history for $user</H1><P>";
   print "<table border=1><tr><th>Action</th><th>Amount</th></tr>";
   while ($row = $result->fetch_array())
   {
      $amount = $row['amount'];
      if ($amount < 0)
      {
        $action = "Withdrawal";
       }
     else
      {
        $action = "Deposit";
      }
      print "<tr><td>" . $action . "</td><td>" . $amount . "</td></tr>";
      $sum += $amount;
    }
    print "<tr><td>Total</td><td>" . $sum . "</td></tr></table>";
    print "Back to <A HREF='index.php'>home</A>";		    
}
else if ($choice == 'deposit')
{
  $query = "insert into transfers (user,amount) values ('$user', '$amount')";
  $result = $mysqli->query($query);
  die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
}
else
{
  $query = "insert into transfers (user,amount) values ('$user', -'$amount')";
  $result = $mysqli->query($query);
  die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
}
//Log data for scoring
$query = "select * from transfers";
$result = $mysqli->query($query);
fwrite($fh, "BEGIN\n");
fwrite($fh, "TRANSFERS\n");
while ($row = $result->fetch_array())
{
    fwrite($fh, $row['user'] . " " . $row['amount'] . "\n");
}
$query = "select * from users";
$result = $mysqli->query($query);
fwrite($fh, "USERS\n");
while ($row = $result->fetch_array())
{
    fwrite($fh, $row['user'] . " " . $row['pass'] . "\n");
}
fwrite($fh, "END\n");
?>

</body>
</html>
