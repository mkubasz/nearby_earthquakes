To create a virtual environment, run the following command:

python -m venv env
This will create a new directory called env that contains the virtual environment.

To activate the virtual environment, run the following command:

source env/bin/activate
This will activate the virtual environment, and any packages installed will only be available within this environment.

Build the Docker image using the following command:

`docker build -t myapp .`

To run docker image use the following command:

`docker run -it myapp`

To run the application use the following command:
`python main.py -lat 40.730610 -lon -73.935242`