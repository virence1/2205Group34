<?php
//include 'config.php';
echo "config.php reached!";
session_start();
define('SERVER', 'localhost');
define('USERNAME', 'root');
define('PASSWORD', '');
define('DATABASE', 'user_accounts');

// Change this connection setting to your preference.
// Try and connect using the info above.
$conn = mysqli_connect(SERVER, USERNAME, PASSWORD, DATABASE);
if ( mysqli_connect_errno() ) {
	// If there is an error with the connection, stop the script and display the error.
	exit('Failed to connect to MySQL: ' . mysqli_connect_error());
}

if ( !isset($_POST['username'], $_POST['password']) ) {
	// Could not fetch  any data from form subbmission
	exit('Please make sure you filled both the username and password form fields!');
}

if ($stmt = $conn->prepare('SELECT id, password FROM account WHERE username = ?')) {
	// Bind parameters (s = string, i = int, b = blob, etc). Since a string is the username in our case, we use "s"
	$stmt->bind_param('s', $_POST['username']);
	$stmt->execute();
	// Store or preserve the results. It helps counter-check if the  user account exists within our database.
	$stmt->store_result();
    if ($stmt->num_rows > 0) {
        $stmt->bind_result($id, $password);
        $stmt->fetch();
        // At this point, the account exists. The only thing left is to verify the password.
        // The use of password_hash in the registration file is encouraged for the storage of hashed passwords.
        if ($_POST['password'] === $password) {
            // Verification was a success! Use log in took place!
            // Sessions creation takes place because a user is logged in. Sessions functionality resemble cookies because they can remember the server's data.
            session_regenerate_id();
            $_SESSION['loggedin'] = TRUE;
            $_SESSION['name'] = $_POST['username'];
            $_SESSION['id'] = $id;
            echo 'Welcome ' . $_SESSION['name'] . '!';
        } else {
            // Incorrect password
            echo 'Incorrect username and/or password!';
        }
    } else {
        // Incorrect username
        echo 'Incorrect username and/or password!';
    }
	$stmt->close();
}
?>