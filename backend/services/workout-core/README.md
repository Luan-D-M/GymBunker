Note: tsx actually skips type checking.  

Warning:
    to change "npm start" from package.json, it is necessary to change the Dockerfile too.
    
    Thats because there are some signal propagation issues with npm when running inside Docker.

* **Reference Article:** [Building Graceful Node Applications in Docker](https://medium.com/@becintec/building-graceful-node-applications-in-docker-4d2cd4d5d392)