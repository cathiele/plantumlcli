#!/bin/bash

# global configuration
export DEMO_PATH="demo"
if [ ! -d ${DEMO_PATH} ]; then
  git clone "https://github.com/HansBug/plantumlcli-testfile.git" ${DEMO_PATH}
fi

export DEAD_FILE_PATH="${DEMO_PATH}/dead_file"
touch ${DEAD_FILE_PATH}
chmod 000 ${DEAD_FILE_PATH}

export DEAD_PATH="${DEMO_PATH}/dead_path"
mkdir -p ${DEAD_PATH}
chmod 000 ${DEAD_PATH}

# demo/jar configuration
export DEMO_JAR_PATH="demo/jar"
mkdir -p ${DEMO_JAR_PATH}

if [ -z "${PRIMARY_JAR_VERSION}" ]; then
  export PRIMARY_JAR_VERSION="1.2020.19"
fi
export PRIMARY_JAR_PATH="${DEMO_JAR_PATH}/plantuml.${PRIMARY_JAR_VERSION}.jar"

if [ -z "${ASSISTANT_JAR_VERSION}" ]; then
  export ASSISTANT_JAR_VERSION="1.2020.16"
fi
export ASSISTANT_JAR_PATH="${DEMO_JAR_PATH}/plantuml.${ASSISTANT_JAR_VERSION}.jar"
