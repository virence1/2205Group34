<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>AC Project</title>
    </head>
    <body>
        <?php
            
            //============== Encrypt of chosen vote ==========================//
            //var_dump($_POST); 
            $vote = $argv[1];
            $username = $argv[2];

            echo "Bruh this better work " . $vote . "  ";
            echo "Bruh this better work " . $username . "  ";

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
            echo $json_payload . "   ";
            
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
            echo "This is the variable json_encoded_vote: " . $json_encoded_vote . "   ";
            echo "The data type for json_encoded_vote is ". gettype($json_encoded_vote) ."   ";

            $pythonNode = 'executeVault.py';
            $node_command = "python3 $pythonNode $json_encoded_vote $username";
            echo "Command: " . $node_command;
            exec($node_command);

        ?>
        <button><a href="/logout">Logout and return</a></button>
    </body>
</html>
