sudo apt-get update
sudo apt-get install -y build-essential
sudo apt-get install -y tcl8.5
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
sudo apt-get -y install gcc
sudo apt-get -y install make
make
make test
sudo make install
cd utils
echo "Y Y Y Y" | sudo ./install_server.sh
sudo update-rc.d redis_6379 defaults
