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

  <style>
    .coffee-container {
      width: 300px;
      height: 280px;
      position: absolute;
      top: calc(50% - 140px);
      left: calc(50% - 150px);
      z-index: 9999
    }
    .coffee-header {
      width: 100%;
      height: 80px;
      position: absolute;
      top: 0;
      left: 0;
      background-color: #ddcfcc;
      border-radius: 10px;
      z-index: 9999
    }
    .coffee-header__buttons {
      width: 25px;
      height: 25px;
      position: absolute;
      top: 25px;
      background-color: #282323;
      border-radius: 50%;
    }
    .coffee-header__buttons::after {
      content: "";
      width: 8px;
      height: 8px;
      position: absolute;
      bottom: -8px;
      left: calc(50% - 4px);
      background-color: #615e5e;
    }
    .coffee-header__button-one {
      left: 15px;
    }
    .coffee-header__button-two {
      left: 50px;
    }
    .coffee-header__display {
      width: 50px;
      height: 50px;
      position: absolute;
      top: calc(50% - 25px);
      left: calc(50% - 25px);
      border-radius: 50%;
      background-color: #9acfc5;
      border: 5px solid #43beae;
      box-sizing: border-box;
    }
    .coffee-header__details {
      width: 8px;
      height: 20px;
      position: absolute;
      top: 10px;
      right: 10px;
      background-color: #9b9091;
      box-shadow: -12px 0 0 #9b9091, -24px 0 0 #9b9091;
    }
    .coffee-medium {
      width: 90%;
      height: 160px;
      position: absolute;
      top: 80px;
      left: calc(50% - 45%);
      background-color: #bcb0af;
      z-index: 9999
    }
    .coffee-medium:before {
      content: "";
      width: 90%;
      height: 100px;
      background-color: #776f6e;
      position: absolute;
      bottom: 0;
      left: calc(50% - 45%);
      border-radius: 20px 20px 0 0;
    }
    .coffe-medium__exit {
      width: 60px;
      height: 20px;
      position: absolute;
      top: 0;
      left: calc(50% - 30px);
      background-color: #231f20;
    }
    .coffe-medium__exit::before {
      content: "";
      width: 50px;
      height: 20px;
      border-radius: 0 0 50% 50%;
      position: absolute;
      bottom: -20px;
      left: calc(50% - 25px);
      background-color: #231f20;
    }
    .coffe-medium__exit::after {
      content: "";
      width: 10px;
      height: 10px;
      position: absolute;
      bottom: -30px;
      left: calc(50% - 5px);
      background-color: #231f20;
    }
    .coffee-medium__arm {
      width: 70px;
      height: 20px;
      position: absolute;
      top: 15px;
      right: 25px;
      background-color: #231f20;
    }
    .coffee-medium__arm::before {
      content: "";
      width: 15px;
      height: 5px;
      position: absolute;
      top: 7px;
      left: -15px;
      background-color: #9e9495;
    }
    .coffee-medium__cup {
      width: 80px;
      height: 47px;
      position: absolute;
      bottom: 0;
      left: calc(50% - 40px);
      background-color: #FFF;
      border-radius: 0 0 70px 70px / 0 0 110px 110px;
    }
    .coffee-medium__cup::after {
      content: "";
      width: 20px;
      height: 20px;
      position: absolute;
      top: 6px;
      right: -13px;
      border: 5px solid #FFF;
      border-radius: 50%;
    }
    @keyframes liquid {
      0% {
        height: 0px;  
        opacity: 1;
      }
      5% {
        height: 0px;  
        opacity: 1;
      }
      20% {
        height: 62px;  
        opacity: 1;
      }
      95% {
        height: 62px;
        opacity: 1;
      }
      100% {
        height: 62px;
        opacity: 0;
      }
    }
    .coffee-medium__liquid {
      width: 6px;
      height: 63px;
      opacity: 0;
      position: absolute;
      top: 50px;
      left: calc(50% - 3px);
      background-color: #74372b;
      animation: liquid 4s 4s linear infinite;
    }
    .coffee-medium__smoke {
      width: 8px;
      height: 20px;
      position: absolute;  
      border-radius: 5px;
      background-color: #b3aeae;
    }
    @keyframes smokeOne {
      0% {
        bottom: 20px;
        opacity: 0;
      }
      40% {
        bottom: 50px;
        opacity: .5;
      }
      80% {
        bottom: 80px;
        opacity: .3;
      }
      100% {
        bottom: 80px;
        opacity: 0;
      }
    }
    @keyframes smokeTwo {
      0% {
        bottom: 40px;
        opacity: 0;
      }
      40% {
        bottom: 70px;
        opacity: .5;
      }
      80% {
        bottom: 80px;
        opacity: .3;
      }
      100% {
        bottom: 80px;
        opacity: 0;
      }
    }
    .coffee-medium__smoke-one {
      opacity: 0;
      bottom: 50px;
      left: 102px;
      animation: smokeOne 3s 4s linear infinite;
    }
    .coffee-medium__smoke-two {
      opacity: 0;
      bottom: 70px;
      left: 118px;
      animation: smokeTwo 3s 5s linear infinite;
    }
    .coffee-medium__smoke-three {
      opacity: 0;
      bottom: 65px;
      right: 118px;
      animation: smokeTwo 3s 6s linear infinite;
    }
    .coffee-medium__smoke-for {
      opacity: 0;
      bottom: 50px;
      right: 102px;
      animation: smokeOne 3s 5s linear infinite;
    }
    .coffee-footer {
      width: 95%;
      height: 15px;
      position: absolute;
      bottom: 25px;
      left: calc(50% - 47.5%);
      background-color: #41bdad;
      border-radius: 10px;
      z-index: 9999
    }
    .coffee-footer::after {
      content: "";
      width: 106%;
      height: 26px;
      position: absolute;
      bottom: -25px;
      left: -8px;
      background-color: #000;
    }
    .coffee-background {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.8); /* semi-transparent white */
      z-index: 9998; /* higher than other elements */
    }
    
    .loading-screen-text {
      position: fixed;
      color:red;
      bottom: 30px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9998;
    }

  </style>

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

  <!-- loading screen -->
  <div class="coffee-container">
      
    <div class="coffee-header">
      <div class="coffee-header__buttons coffee-header__button-one"></div>
      <div class="coffee-header__buttons coffee-header__button-two"></div>
      <div class="coffee-header__display"></div>
      <div class="coffee-header__details"></div>
    </div>
    <div class="coffee-medium">
        <div class="coffe-medium__exit"></div>
        <div class="coffee-medium__arm"></div>
        <div class="coffee-medium__liquid"></div>
        <div class="coffee-medium__smoke coffee-medium__smoke-one"></div>
        <div class="coffee-medium__smoke coffee-medium__smoke-two"></div>
        <div class="coffee-medium__smoke coffee-medium__smoke-three"></div>
        <div class="coffee-medium__smoke coffee-medium__smoke-for"></div>
        <div class="coffee-medium__cup"></div>
    </div>
    <div class="coffee-footer"></div>
    <div class="coffee-background">
      <h2 class="loading-screen-text">Your Vote is now being processed, please do not refresh the page.</h2> 
    </div>
  </div>

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