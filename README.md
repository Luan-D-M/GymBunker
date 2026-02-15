# GymBunker

Running:

(Docker version >= 24.0.0)
```
docker compose --profile ui up  
```


# Tests
```
docker compose run --rm workout-core npm test
```

```
docker compose run --rm authenticator ./run-tests.sh
```