<html>
<body>

<?php

$myFile = "/tmp/request.log";
$fh = fopen($myFile, 'a');
if (!$fh) {
   echo "opening '$myFile' failed";
   exit;
}

$user = clear_input($_GET["user"]);
$pass = clear_input($_GET["pass"]);
$amount = (int)clear_input($_GET["amount"]);
$choice = clear_input($_GET["drop"]);

if (is_null($user) || is_null($pass) || is_null($choice)) {
  print "Error: all the fields must be filled";
  print "Back to <A HREF='index.php'>home</A>";	
} else if (!ctype_alnum($user)) {
  print "Error: username can only contain alphanumeric characters.";
  print "Back to <A HREF='index.php'>home</A>";	
} else if (strlen($user) > 20) {
  print "Error: username must contain less than 20 characters."; // Increase the size in the db?
  print "Back to <A HREF='index.php'>home</A>";	
} else if (strlen($pass) < 8 || strlen($pass) > 50) {
  print "Error: password must be contain 8 to 50 characters.";
  print "Back to <A HREF='index.php'>home</A>";	
} else if (!is_numeric($amount) || ($amount <= 0 && ($choice == "deposit" || $choice == "withdraw"))) {
  print "Error: amount must be above 0.";
  print "Back to <A HREF='index.php'>home</A>";	
} else if ($amount >= 2147483648) {
  print "Error: amount is too big.";
  print "Back to <A HREF='index.php'>home</A>";
}
else {
  $mysqli = new mysqli('localhost', 'root', 'rootmysql', 'ctf2');
  if (!$mysqli) 
  {
    die('Could not connect: ' . $mysqli->error());
  }
  $url="process.php?user=$user&pass=$pass&drop=balance";
  if ($choice == 'register')
  {
    $command = escapeshellcmd("python3 sign_up.py " . $user . " " . $pass);
    $output = shell_exec($command);
    die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
  }
  else if ($choice == 'balance')
  {
    if(!authenticate($user, $pass)) {
      die("Error: username and/or password is incorrect.\n");
      print "Back to <A HREF='index.php'>home</A>";	
    } else {
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
  }
  else if ($choice == 'deposit')
  {
    if(!authenticate($user, $pass)) {
      die("Error: username and/or password is incorrect.\n");
      print "Back to <A HREF='index.php'>home</A>";	
    } else {
      $stmt = $mysqli->prepare("insert into transfers (user,amount, tstamp) values (?, ?, now())");
      $stmt->bind_param("si", $user, $amount);
      $stmt->execute();
      $result = $stmt->get_result();
    }
    die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
  }
  else if ($choice == 'withdraw')
  {
    if(!authenticate($user, $pass)) {
      die("Error: username and/or password is incorrect.\n");
      print "Back to <A HREF='index.php'>home</A>";	
    } 
    else {
      $stmt = $mysqli->prepare("select * from transfers where user=?");
      $stmt->bind_param("s", $user);
      $stmt->execute();
      $result = $stmt->get_result();
      $sum = 0;
      while ($row = $result->fetch_array())
      {
          $tmp_amount = $row['amount'];
          if ($tmp_amount < 0)
          {
            $action = "Withdrawal";
          }
        else
          {
            $action = "Deposit";
          }
          $sum += $tmp_amount;
      }
      if($sum >= $amount) {
        $amount = -$amount;
        $stmt = $mysqli->prepare("insert into transfers (user, amount, tstamp) values (?, ?, now())");
        $stmt->bind_param("si", $user, $amount);
        $stmt->execute();
        $result = $stmt->get_result();
	      die('<script type="text/javascript">window.location.href="' . $url . '"; </script>');
      }
      else {
        die("Error: unsufficient funds.\n");
        print "Back to <A HREF='index.php'>home</A>";
      }
    }
  }
  else {
    die("Error: Unrecognized action.\n");
    print "Back to <A HREF='index.php'>home</A>";	
  }
  //Log data for scoring
  $query = "select * from transfers";
  $result = $mysqli->query($query);
  fwrite($fh, "BEGIN\n");
  fwrite($fh, "TRANSFERS\n");
  while ($row = $result->fetch_array())
  {
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

  fclose($fh);
}

function clear_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

function authenticate($user, $pass) {
  $command = escapeshellcmd("python3 login.py " . $user . " " . $pass);
  $output = shell_exec($command);
  if(strpos($output, "True") !== false) {
    return TRUE;
  }
  else {
    return FALSE;
  }
}
?>

</body>
</html>
