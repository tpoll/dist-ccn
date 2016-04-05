sudo apt-get update
sudo apt-get -y install gcc
sudo apt-get -y install libssl-dev
sudo apt-get -y install make
mkdir probe
touch probe/index.html
cd probe && python -m SimpleHTTPServer > /dev/null 2>&1
git clone https://github.com/cn-uofbasel/ccn-lite
git clone https://github.com/tpoll/dist-ccn
git clone https://github.com/redis/hiredis
cd /home/todd/hiredis/ && sudo make && sudo make install
cd /home/todd/dist-ccn/src/ && make
cd /home/todd/ccn-lite/src/ && make
sudo ldconfig
