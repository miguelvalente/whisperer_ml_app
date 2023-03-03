# whisperer_ml_app

This the repo for developing a user friendly frontend for the [whisperer_ML](https://github.com/miguelvalente/whisperer).

Built with [Streamlit](https://streamlit.io/).

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)

### Installing

You can either pull the image from Docker Hub or build locally.
- Pulling from Docker Hub
```
docker pull miguelvalente/whisperer_ml_app
```
### Running

1. Make the following folder structure

```
│── /data
│   ├── archives
│   ├── converted_files
│   ├── datasets
│   └── raw_files
```

2. Run docker
```
docker run  -v data:/home/data -p 8501:8501 whisperer_ml_app
```
The ```-v data:/home/data``` mounts the ```data``` directory you just made into the specified path inside the Docker container. This type of volume mounting is called __host volume__.

3. You're done and you can access the app at ```localhost:8501```.
