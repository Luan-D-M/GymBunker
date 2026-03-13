# GymBunker
GymBunker is a web application for gym workout management built on a **microservices architecture**. It focuses on scalability and robust backend communication, utilizing different technologies and databases for distinct services.


##  Tech Stack
* **Frontend:** Vue.js
* **Backend Services:** Node.js (TypeScript), Python (FastAPI)
* **API & Communication:** REST API, gRPC
* **Databases:** PostgreSQL, MongoDB
* **Infrastructure & Proxy:** Docker, NGINX
* **CI/CD:** GitHub Actions


##  Quick Start
### Running:

(Docker version >= 24.0.0)
```
docker compose --profile ui up  
```


### Tests:
```
docker compose run --rm workout-core npm test
```

```
docker compose run --rm authenticator ./run-tests.sh
```