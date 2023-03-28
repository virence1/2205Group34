
![Logo](https://ourworldindata.org/uploads/2023/01/Thumbnail-Democracy_Blue_01-768x402.png)


# Digital Democracy Defenders

We have taken inspiration from the Tor network, and applied the underlying concepts to our application. The Tor network has the entry, middle and exit relays, similar to our application where we have multiple nodes (N1, N2, N3) that serve different purposes in the overall encryption of the payload. 

The route that the payload will take is randomised. This means that the path will never be the same. In one instance, the payload could go from N1 > N2 > N3, and another time it could go from N2 > N1 > N3. This gives us more layers of security due to the lower predictability of what layers of encryption that payload could go through. 

For our proof of concept, we are using three different key-exchange algorithms, namely Diffie Hellman, RSA and AES. For future implementations on an actual production system, we can opt for more algorithms to be included for even more security. As such, adding more algorithms essentially adds more layers of “onions” like in the Tor onion concept above.

## Features

- Multiple Nodes: Inspired by the Tor network's entry, middle, and exit relays, our application utilises multiple nodes (N1, N2, N3) to serve different purposes in the overall encryption of the payload.

- Randomised Routing: The payload can take various paths, such as N1 > N2 > N3 or N2 > N1 > N3, increasing the security of the payload due to unpredictability.

- Multiple Key-Exchange Algorithms: Our proof of concept uses three different key-exchange algorithms: Diffie-Hellman, RSA, and AES. This provides an additional layer of security.

## 🚀 Prerequisites 
For you to run this project on your own you would need the following set up before hand

- 5 Ubuntu 22.04 VM in the Azure Portal
- Azure Key Vault
- Azure Active Directory 
- Follow the instructions at the link given at the end of the section to set up all 5 Ubuntu 22.04 VMs for a basic Flask application
-  Pip install required dependencies and packages on each Ubuntu 22.04 VM according to the requirements.txt file
 - Increase Gunicorn timeout for  all 5 Ubuntu 22.04 VMs once intial server setup is done
 - Ensure that all of it is done before proceeding to run the application 
 https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04
## Setting up the Azure Key Vault and Directory (Running on your own)

💬 Create an Azure Key Vault on the Azure Portal by following the official documentation by Microsoft
>`https://learn.microsoft.com/en-us/azure/key-vault/general/quick-create-portal`

## Deployment

To deploy this project:
- Boot up 5 virtual machines which are Ubuntu 22.04: live, node1, node2, node3, destination.
- Extract the zip file provided according to the folder of each virtual machine name.
- Enter these commands on each node:


```bash
#sudo apt update
#sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
#sudo python3-venv
#mkdir ~/<node>
#cd ~/<node>
#python3 -m venv <node>
#source <node>/bin/activate
#pip install wheel gunicorn flask
#cd ~/<node>
#gunicorn --bind 0.0.0.0:5000 wsgi:app
#deactivate
#sudo nano /etc/systemd/system/<node>.service
```
<node>.service file
```
[Unit]
Description=Gunicorn instance to serve <node>
After=network.target
[Service]
User=<user>
Group=www-data
Environment="PATH=/home/<user>/<node>/<node>env/bin"
ExecStart=/home/<user>/<node>/<node>env/bin/gunicorn --workers 3 --bind unix:<node>.sock -m 007 wsgi:app
[Install]
WantedBy=multi-user.target
```

```bash
#sudo systemctl start <node>
#sudo systemctl enable <node>
#sudo nano /etc/nginx/sites-available/<node>
```
/etc/nginx/sites-available/<node> file
```
server {
    listen 80;
    server_name <domain> www.<domain>;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/<user>/<node>/<node>.sock;
    }
}
```
```bash
#sudo ln -s /etc/nginx/sites-available/<node>/etc/nginx/sites-enabled
#sudo systemctl restart nginx
```

Install the following dependencies and packages on each nodes
```bash
#source <node>env/bin/activate
#pip install azure-common azure-core azure-identity azure-keyvault-keys azure-keyvault-secrets
```

Increase the Gunicorn timeout
```bash
#cd /home/<user>/<node>/<node>env/lib/python3.8/site-packages/gunicorn
#nano config.py
```
