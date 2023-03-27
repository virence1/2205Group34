<!DOCTYPE html>
<html>
    <head>

        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>AC Project</title>
        <link href='http://fonts.googleapis.com/css?family=Ropa+Sans' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=Source+Sans+Pro' rel='stylesheet' type='text/css'>
        <script src = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
        
        <link href="../../static/css/styles.css"rel='stylesheet' type="text/css">
        <script src="../static/js/app.js" type="text/javascript"></script>
        
    </head>
    <body>
        
        <?php
                
            //============== Encrypt of chosen vote ==========================//
            //var_dump($_POST); 
            $vote = $argv[1];
            $username = $argv[2];
            
            // Generate a secure encryption key and initialization vector (IV)
            $key = openssl_random_pseudo_bytes(32); // 32-byte key for AES-256 encryption
            $iv = openssl_random_pseudo_bytes(16); // 16-byte IV
            
            // Encrypt the vote using AES-256-CBC
            $encrypted_vote = openssl_encrypt($vote, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);
            $iv_base64 = base64_encode($iv); // Convert IV to base64 for easier storage and transport
            
            // Create the JSON payload
            $data = array(
            
                'vote' => base64_encode($encrypted_vote),
                'key' => base64_encode($key),
                'iv' => base64_encode($iv),
                'user'=> $username
            );
            
            $json_payload = json_encode($data);
        
                        
            // ==== Parsing variables from PHP to python ===== //
            // Save the JSON payload into a temporary file
            $temp_file = $username . '_temp_payload.json';
            file_put_contents($temp_file, $json_payload);
            
            // Run the Python script with the temporary file as an argument
            $python_script = 'keyGeneration.py';
            $command = "python3 $python_script $temp_file";
            exec($command);
            
            // Delete the temporary file
            unlink($temp_file);
            
            $json_encoded_vote = base64_encode($encrypted_vote);
            
            $pythonNode = 'executeVault.py';
            $node_command = "python3 $pythonNode $json_encoded_vote $username";
            exec($node_command);
            
            $jsonData = file_get_contents('resultStatus.json');
            // Convert the JSON data to a PHP array
            $data = json_decode($jsonData, true);
            $node_response = $data['returnResponse'];
            
            /* Debugging echoes */
            // echo "Bruh this better work " . $vote . "  ";
            // echo "Bruh this better work " . $username . "  ";
            // echo $json_payload . "   ";
            //echo "This is the variable json_encoded_vote: " . $json_encoded_vote . "   ";
            // echo "The data type for json_encoded_vote is ". gettype($json_encoded_vote) ."   ";
            // echo "Command: " . $node_command;
            // echo "node_response: " . $node_response;
            
        ?>
        <div class="panel-wrap">
            <div class="panel-wrapper">
                <div class="confirmation-message">
                    <?php

                        if($node_response != NULL){
                            if($node_response == "10UWU3030UWU32322020UWU404050" or 
                            $node_response == "30UWU32322020UWU1010UWU404050" or 
                            $node_response == "20UWU3030UWU32321010UWU404050" or 
                            $node_response == "10UWU2020UWU3030UWU3232404050" or 
                            $node_response == "20UWU1010UWU3030UWU3232404050" or 
                            $node_response == "30UWU32321010UWU2020UWU404050"){

                                $pythonDatabase = 'updateDatabase.py';
                                $database_command = "python $pythonDatabase $username";
                                exec($database_command);

                                echo "<h1>Thank you for your vote!</h1>";
                                echo "<p>Your vote has been successfully recorded.</p>";
                                echo "<button><a href='/logout'>Logout and return</a></button>";


                            } else {
                                echo "<h1>Error, Vote has not been recorded!</h1>";
                                echo "<p>Error Status: " . $node_response . "</p>";
                                echo "<button><a href='/logout'>Logout and try again</a></button>";
                            }

                        }else {
                            echo "<h1>Error, Vote has not been recorded!";
                            echo "<p>Error Status: </p>" . $node_response;
                        }
                    ?>
                </div>
            </div>
        </div>
    </body>
</html>
