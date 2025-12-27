Requirements:
    Python >= 3.12


Running the Unit Tests:
    Run it with CWD: ./authenticator, in other words, run it from where
    this README.md file is.
    
  ./run-tests.sh




PS: Key pair for JWT generated with 
```
ssh-keygen -t rsa -b 4096 -m PEM -f ./keys/jwtRS256.key
openssl rsa -in ./keys/jwtRS256.key -pubout -outform PEM -out ../../keys/jwtRS256.key.pub
```