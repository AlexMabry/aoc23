# Advent of Code 2023

## Setup

### Install dependencies
    
    poetry install

### Login to advent of code

    Go to: https://adventofcode.com/ and login with your account

### Get AOC token from browser cache

    mkdir -p ~/.config/aocd
    aocd-token > ~/.config/aocd/token

### Generate all files using the template

    poetry run generate

## Usage

### Test solution against the examples

    poetry run test [DAY]

### Solve puzzle

    poetry run solve [DAY]

