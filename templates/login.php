<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Login Page</title>
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.1/css/all.css">
		<link rel="stylesheet" href="{{ url_for('static', filename='css/loginstyles.css') }}">
	</head>
	<body>
		<div class="login">
			<h1>LOGIN</h1>
			<form action="/authenticate" method="POST">
				<label for="username">
					<i class="fas fa-user"></i>
				</label>
				<input type="text" name="username" placeholder="Username" id="username" required>
				<label for="password">
					<i class="fas fa-lock"></i>
				</label>
				<input type="password" name="password" placeholder="Password" id="password" required>
				<!--extra line to grab cookie-->
				<input type="hidden" name="token" value="<?php echo $_COOKIE['token']; ?>">
				<input type="submit" value="Login">
			</form>
		</div>
	</body>
</html>