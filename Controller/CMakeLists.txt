cmake_minimum_required(VERSION 3.15)

# Chemin vers la toolchain Arduino CMake
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/cmake/cmake/ArduinoToolchain.cmake)

# Configuration de la carte Arduino
set(ARDUINO_BOARD "arduino:avr:uno")

# Nom du projet
project(ArduinoProject)

# Fichiers source
set(SRCS
        src/main.ino
)

# Générer le firmware Arduino
generate_arduino_firmware(${CMAKE_PROJECT_NAME}
        SRCS ${SRCS}
)
