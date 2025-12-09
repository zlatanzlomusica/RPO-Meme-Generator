# RPO-Meme-Generator
Online meme generator.

Ta repozitorij vsebuje preprosto Flask aplikacijo za generiranje memov, zapakirano v Docker kontejner.

## Zagon Aplikacije z Dockerjem
Korak za zagon aplikacije s pomočjo Dockerja.

### Predpogoji
Imate nameščen Docker (Docker Desktop).

### Zagon aplikacije  

V korenskem direktoriju projekta (kjer se nahaja `Dockerfile`) izvedite ta ukaz:


### Ukazi
```bash
docker build -t rpo .
docker run -p 5000:5000 --name meme-app-debug rpo