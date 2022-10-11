# Meduzzen_intership
How to run a project?
```
uvicorn app.main:app --reload
```

How to run a project with a docker?
```
docker build -t myimage .
docker run --name <container name> -p 80:80 myimage
```
