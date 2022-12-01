<html>
<body>

<?php

$myFile = "/tmp/request.log";
$fh = fopen($myFile, 'a');

$user = clear_input($_GET["user"]);
$pass = clear_input($_GET["pass"]);
$amount = (int)clear_input($_GET["amount"]);
$choice = clear_input($_GET["drop"]);

if (is_null($user) || is_null($pass) || is_null($amount) || is_null($choice) || 
    !is_numeric($amount) || !ctype_alnum($user)) {
  print "Error: Please check your inputs";
} else {
  $mysqli = new mysqli('localhost', 'root', 'rootmysql', 'ctf2');
  if (!$mysqli) 
  {
    die('Could not connect: ' . $mysqli->error());
  }
  $url="process.php?user=$user&pass=$pass&drop=balance";
  if ($choice == 'register')
{
  if(strlen($pass) < 8 || strlen($pass)>100) {
  die('Error: the password must be 8 to 100 characters');
  }	
  if(strlen($user) > 100) {
  die('Error: the username must be less that 100 characters');
  }

    $stmt = $mysqli->prepare("insert into users (user,pass) values (?, ?)");
    $stmt->bind_param("ss", $user, $pass);
    $stmt->execute();
    $result = $stmt->get_result();
    die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
  }
  else if ($choice == 'balance')
{
  // todo add authentication
    $stmt = $mysqli->prepare("select * from transfers where user=?");
    $stmt->bind_param("s", $user);
    $stmt->execute();
    $result = $stmt->get_result();
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
  // todo add authentication
    $stmt = $mysqli->prepare("insert into transfers (user,amount) values (?, ?, now())");
    $stmt->bind_param("si", $user, $amount);
    $stmt->execute();
    $result = $stmt->get_result();
    die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
  }
  else if ($choice == 'withdraw')
{
  // todo add authentication
    $stmt = $mysqli->prepare("insert into transfers (user,amount) values (?, ?, now())");
    $stmt->bind_param("si", $user, -$amount);
    $stmt->execute();
    $result = $stmt->get_result();
    die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
  }
  else {
    print "Error: Unrecognized action";
  }
  //Log data for scoring
  $query = "select * from transfers";
  $result = $mysqli->query($query);
  fwrite($fh, "BEGIN\n");
  fwrite($fh, "TRANSFERS\n");
  while ($row = $result->fetch_array())
  {
      $timestamp = date('Y-m-d h:i:s', time());
      fwrite($fh, $row['user'] . " " . $row['amount'] . " " . $row['tstamp'] . "\n");
  }
  $query = "select * from users";
  $result = $mysqli->query($query);
  fwrite($fh, "USERS\n");
  while ($row = $result->fetch_array())
  {
      fwrite($fh, $row['user'] . " " . $row['pass'] . "\n");
  }
  fwrite($fh, "END\n");
}

function clear_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}
?>

</body>
</html>
