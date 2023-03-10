# animalinfo
School project to recognize an animal from an image and give information about it.

It's currently trained to recognize:
- Capybaras
- Cats
- Dogs
- Frogs
- Pigs
- Rabbits
- Snakes

## [Demonstration](https://i.imgur.com/6S2eJtJ.mp4)

## Requirements
- Python 3.10 (tensorflow is not yet compatible with 3.11); a [Conda](https://docs.conda.io/en/latest/) `environment.yml` file is included for people who have 3.11 installed and don't want multiple versions (you'll still have to install pymediawiki with pip).
- An API key from [Machine Learning for Kids](https://machinelearningforkids.co.uk/).
- A GitHub [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with the `repo` scope

## Usage
- Create a file named `.env` and write in it

  ```
  API_KEY = <your api key>
  GITHUB_TOKEN = <your personal access token>
  ```

- Install required packages with `pip install -r requirements.txt`
- Run the program with `python animalinfo.py`
