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

## Advanced: CI using GitHub Actions

It is also possible to implement continuous integration using GitHub Actions and have tests running on every push.

To do that, create the `.github/workflows/compile-and-tests.yml` file and place the following in there:

```yml
name: CI
on: push

jobs:
  compile-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout project
        uses: actions/checkout@v2
        with:
          path: 'project'
      - name: Setup JDK 16
        uses: actions/setup-java@v2
        with:
          distribution: 'adopt'
          java-version: 16
      - name: Place po-uilib in correct folder and compile it
        working-directory: project
        run: wget https://web.tecnico.ulisboa.pt/\~david.matos/w/pt/images/3/37/Po-uilib-202109221024.tar.bz2 && tar xvf Po-uilib-202109221024.tar.bz2 && mv po-uilib-202109221024 po-uilib && rm Po-uilib-202109221024.tar.bz2 && cd po-uilib && make && cd ..
      - name: Run makefile
        working-directory: project
        run: make compile
      - name: Checkout tests
        uses: actions/checkout@v2
        with:
          repository: diogotcorreia/proj-ist-unit-tests
          path: 'tests'
      - name: Configure tests
        working-directory: tests/po/2021-2022/po-p1
        run: echo "PROJECT_CLASSPATH=$(cd $GITHUB_WORKSPACE/project && echo "$(pwd)/po-uilib/po-uilib.jar:$(pwd)/ggc-app/ggc-app.jar:$(pwd)/ggc-core/ggc-core.jar")" > config
      - name: Run tests
        working-directory: tests/po/2021-2022/po-p1
        run: make
```

For this to work, you must either have a `Makefile` with the `compile` target, or edit the action accordingly.  
This workflow also supposes that your makefiles use the `po-uilib` folder (but it's ignored, so not commited to the repository).
This can be changed in the action above, if you have a different setup.  
You can also change the CLASSPATH if appropriate.

An example `Makefile` for the whole repository would be:

```make
GGC_CORE_PATH=./ggc-core
GGC_APP_PATH=./ggc-app
CLASSPATH=$(shell pwd)/po-uilib/po-uilib.jar:$(shell pwd)/ggc-app/ggc-app.jar:$(shell pwd)/ggc-core/ggc-core.jar

all: compile
	CLASSPATH=$(CLASSPATH) java ggc.app.App
compile::
	$(MAKE) $(MFLAGS) -C $(GGC_CORE_PATH)
	$(MAKE) $(MFLAGS) -C $(GGC_APP_PATH)
clean:
	$(MAKE) $(MFLAGS) -C $(GGC_CORE_PATH) clean
	$(MAKE) $(MFLAGS) -C $(GGC_APP_PATH) clean
```
