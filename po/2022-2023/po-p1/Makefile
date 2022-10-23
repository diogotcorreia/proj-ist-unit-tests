CONFIG=config
include ${CONFIG}
TESTS_CLASSPATH=tests

all: junit.jar compile
	java -jar junit.jar -cp "$(PROJECT_CLASSPATH):$(TESTS_CLASSPATH)" -scan-classpath --disable-banner

compile:
	CLASSPATH="$(PROJECT_CLASSPATH):junit.jar" javac -encoding UTF-8 `find . -name \*.java`

clean:
	$(RM) `find . -name \*.class`

junit.jar:
	wget https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.9.0/junit-platform-console-standalone-1.9.0.jar -O junit.jar
