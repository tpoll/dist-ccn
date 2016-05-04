#Install and compile ccn nodes
sudo apt-get update
sudo apt-get -y install gcc
sudo apt-get -y install libssl-dev
sudo apt-get -y install make
git clone https://github.com/cn-uofbasel/ccn-lite
git clone https://github.com/tpoll/dist-ccn
git clone https://github.com/redis/hiredis
cd ~/hiredis/ && sudo make && sudo make install
cd ~/dist-ccn/src/ && make
cd ~/ccn-lite/src/ && make
sudo ldconfig

cd
export CCNL_HOME="/home/todd/dist-ccn"
echo " hello world" | ($CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/ndn/test/mycontent" > $CCNL_HOME/test/ndntlv/mycontent.ndntlv)
./server > slog.txt &
sudo sh create_start_script.sh