[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
![Tests](https://github.com/jfuruness/labs/actions/workflows/tests.yml/badge.svg)

# labs

This package creates a FastAPI service to use as a labs for Dr. Herzberg's cybersecurity books with SQL as a database.

- [labs](#labs)
  - [Package Description](#package-description)
  - [Installation](#installation)
  - [Usage](#usage)
      - [For developers: How to add a lab](#for-developers-how-to-add-a-lab)
  - [Testing](#testing)
  - [Development/Contributing](#developmentcontributing)
  - [Credits](#credits)
  - [License](#license)

## Package Description


This package creates a FastAPI service to use as a labs for Dr. Herzberg's cybersecurity books with SQL as a database.

Downloading the source via github will enable you to run each lab file locally. They boast full functionality, being able to generate and grade labs as needed for someone learning on their own.


## Installation
* [labs](#labs)

Install python and pip if you have not already.
NOTE: This repo requires python >= 3.12

Then run:

```bash
pip3 install pip --upgrade
pip3 install wheel
git clone https://github.com/jfuruness/labs.git
cd labs
pip3 install -e .
```

To test the development package: [Testing](#testing)


## Usage
* [labs](#labs)

Once installed, to generate a lab locally, cd into a given folder (ie: src/labs/DownloadLab) and run main.py

This automatically generated the selected lab files and instructions.

Additionally, there are several flags you can use to configure output. To specify a flag prefix it with two dashes ("--") plus the flag name. 

A list of available flags is shown below.

| Flag              | Description | Value |
| :---------------- | :-------------------------------------------: | --------: |
| out               |   Sets the output directory when generating a lab to a specified one.   | any valid path/directory |
| in                |   Sets the directory to look for solutions when attempting to grade a lab   | any valid path/directory |

If you want to use the flag system you need to specify the mode in which you are running the lab file. There are currently two modes, gen, and grade. Gen generates the lab files, and grade looks for a solution folder to grade against it's automatic grading scheme. 

A completed example of the flag system is as follows:
```bash
python3 src/labs/DownloadLab/main.py gen --out 'some directory' -> for generating to a specific directory

python3 src/labs/DownloadLab/main.py grade --in 'some directory' -> for grading from a specific submission
```

#### For developers: How to add a lab

Labs are placed within labs/src/labs.
After seeding the lab, it is given a specific lab_template_id, which is later used in the LabTemplate subclass.
Each lab has a questions folder, a solutions folder, and a lab_template.py file containing a subclass of LabTemplate
LabTemplate must generate a unique lab for each student.
LabTemplate saves the seed used for this, along with the solution, and a few other items, which can then be used for each individual student.
You can see a list of abstract methods that need to be implemented in the labs/labs/utils/lab_template.py file.
You can also see an example of this implementation in labs/labs/labs/tls/

NOTE: once you have implemented your lab, you must add an ```__init__.py``` file.
You also must modify ```labs/labs/labs/__init_.py``` file so that your lab template is both imported and added to the lab_templates tuple that exists within that file

Other than that, you should be good to go!


## Testing
* [labs](#labs)

To test the package after installation:

```
cd labs
pytest labs
ruff labs
black labs
mypy labs
```

If you want to run it across multiple environments, and have python 3.12 installed:

```
cd labs
tox
```


## Development/Contributing
* [labs](#labs)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Add an engine test if you've made a change in the simulation_engine, or a system/unit test if the simulation_framework was modified
5. Run tox (for faster iterations: flake8, mypy, and pytest can be helpful)
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin my-new-feature`
8. Ensure github actions are passing tests
9. Email me at jfuruness@gmail.com

## Credits
* [labs](#labs)


Thanks to Dustin for the original implementation of this and to Amir for assisting in this independent study.

## License
* [labs](#labs)

BSD License (see license file)
