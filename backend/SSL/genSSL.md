# Command to generate SSL Cert, do this in SSL folder
```bash
openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -out certificate.pem -keyout privatekey.pem
```