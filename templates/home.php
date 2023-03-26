<?php
session_start();
$username = $argv[1];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <?php
    include 'common/head.html';
  ?>
  <script src="../static/js/app.js"></script>
</head>
<body>
  
  <!--- header div start -->
  <div class="header">
    <div class="header-left-panel">
      <div class="logo-wrap">
        <div class="logo">
          <h2>"YOUR VOTE MATTERS"</h2>
          <h1>Digital Democracy Defenders</h1>
        </div>
      </div>
    </div>
    <div class="header-right-panel">
      <div class="header-right-panel-top">
        <p>Call Us : 6592 2030
        <p> <a href="#">Mail Us : 2102536@sit.singaporetech.edu.sg</a> 
      </div>
      <div class="menu">
        <ul>
          <li class="marRight20"><a href="/index">home</a></li>
          <li class="marRight20"><a href="/about">about</a></li>
          <li><a href="/logout">logout</a></li>
          <li class="marRight20"><a href="#"><?php echo $username ?></a></li>
        </ul>
      </div>
    </div>
  </div>
  <!--- header div end -->
  <!-- body start-->
  <div class="panel-wrap">
    <div class="panel-wrapper">
      <div class="panel marRight30"id="vote-button">
        <div class="img">
          <img src="../static/images/candidate-1.jpg" width="250" height="250"/>
        </div>
        <div class="title">
          <h1>Jasminka Jurković</h1>
        </div>
        <div class="border"></div>
        <div class="content">
          <p>"Independent Candidate"</p>
          <form class="voting-form" action="/vote" method="post">
            <input type="hidden" name="account_username" id="account_username" value="<?php echo $username; ?>">
            <button type="submit" value="Jasminka Jurkovic" class="button button1 marLeft70" name="vote_value" id="vote_value">Vote</button>
          </form>
        </div>
      </div>
      <div class="panel marRight30"id="vote-button">
        <div class="img">
          <img src="../static/images/candidate-2.jpg" width="250" height="250"/>
        </div>
        <div class="title">
          <h1 class="border-bottom">Ray Pineda Alcaraz</h1>
        </div>
        <div class="border"></div>
        <div class="content">
          <p>"Representing the XYZ Party"<br/></p>
          <form class="voting-form" action="/vote" method="post">
            <input type="hidden" name="account_username" id="account_username" value="<?php echo $username; ?>">
            <button type="submit" value="Ray Pineda Alcaraz" class="button button1 marLeft70" name="vote_value" id="vote_value">Vote</button>
          </form>
        </div>
      </div>
      <div class="panel">
        <div class="img">
          <img src="../static/images/candidate-3.jpg" width="250" height="250"/>
        </div>
        <div class="title">
          <h1 class="border-bottom">Asmarina Luwam</h1>
        </div>
        <div class="border"></div>
        <div class="content">
          <p>"Representing the ABC party"</p>
          <form class="voting-form" action="/vote" method="post">
            <input type="hidden" name="account_username" id="account_username" value="<?php echo $username; ?>">
            <button type="submit" value="Asmarina Luwam" class="button button1 marLeft70" name="vote_value" id="vote_value">Vote</button>
          </form>
        </div>
      </div>
    </div>  
  </div>
  
  <!--- page wrap div end (modify end) -->
  <footer class ="footer">
    <p>Copyright (c) 2205 Group 34. All rights reserved. <a href="http://www.alltemplates.com">< www.alltemplateneeds.com ></a></p>
  </footer>
</body>
</html>