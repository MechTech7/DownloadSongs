#TODO: Add support for MacOS as well
info=$(uname)
if [ $info='Darwin' ];
then
  easy_install pip
  pip install beautifulsoup4
  pip install pafy
else
  apt-get install python-pip
  pip install beautifulsoup4
  pip install pafy
fi
