#! /bin/bash

`xcode-select --install`

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install snappy
brew install ta-lib

cd environments/macos
source create.sh
source activate qtc
source install.sh
rqalpha update_bundle
cd ..
