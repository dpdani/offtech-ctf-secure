<html>
<body>

<form action="<?php echo htmlspecialchars('process.php');?>" method="post">
Username: <input type="text" name="user">
Password: <input type="text" name="pass">
Amount: <input type="text" name="amount">
Action: <select name='drop'>
  <option value='balance'>Balance and transfer history</option>
  <option value='register'>Register</option>
  <option value='deposit'>Deposit</option>
  <option value='withdraw'>Withdraw</option>
</select>
<input type="submit">
</form>

</body>
</html>
