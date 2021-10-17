# Warehouse Manager PO - Tests

This folder contains tests for the 1st (and only) project (Warehouse Manager) for PO 2020/2021.

## Using this in your own project

To use this to test your own project, here are the requisites you must meet:

- Be running a Unix system (Linux or MacOS). This should also work on a VM and WSL.
- Have built the `gcc-app.jar`, `ggc-core.jar` and `po-uilib.jar` jars.
- Have `git`, `java` (>= 14.0.0) and `make` installed on your system (probably already installed).

### Clone this repository

Start by cloning this repository using `git`.  
**DO NOT CLONE THIS INSIDE YOUR OTHER PROJECT FOLDER, ESPECIALLY IF THAT'S ALSO A GIT REPOSITORY**  
You can clone this anywhere in your system (other than your project folder).

```bash
git clone https://github.com/diogotcorreia/proj-ist-unit-tests.git
```

### Method 2: Make files (more complex to setup but more efficient)

#### Configure

Then, you have to create the configuration file.
To do that, copy the `config.default` file to `config` and edit it accordingly.

```bash
cd proj-ist-unit-tests/po/2021-2022/po-p1 # go into this projet's folder inside the repository's folder if you haven't already
cp config.default config # create the configuration file from the default
nano config # edit the file as you'd like. You can use another editor, like 'vim', 'code', etc.
```

The `CLASSPATH` must be set to your JARs. For example:

```
PROJECT_CLASSPATH=/home/diogo/Documents/ist/po/project/po-uilib/po-uilib.jar:/home/diogo/Documents/ist/po/project/ggc-app/ggc-app.jar:/home/diogo/Documents/ist/po/project/ggc-core/ggc-core.jar
```

#### Run the tests

To run the tests, just run `make` in this repository's folder:

```bash
make
```

This will download the testing framework (JUnit) if it hasn't already, and then execute the tests.  
The test program will give detailed results when tests fail.

### Update the tests

The tests will be updated frequently on this repository.
To make sure you're running an up-to-date copy, just pull from the repository using:

```bash
git pull
```

### Contribute

Community tests are _extremely_ welcome!
Feel free to submit a PR.
