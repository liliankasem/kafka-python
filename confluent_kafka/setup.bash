#Installing everything you need
echo "Installing necessary libraries and downloading repos"
sudo apt-get install git openssl libssl-dev build-essential python-pip python-dev librdkafka-dev
git clone https://github.com/confluentinc/confluent-kafka-python
git clone https://github.com/edenhill/librdkafka
echo "Setting up librdkafka"
cd librdkafka
./configure
make
sudo make install
cd ..
echo "Setting up Confluent's Python Kafka library"
#The "/" at the end of confluent-kafka-python is important
#If there's no "/" pip will try to download a confluent-kafka-python package and fail to find it
sudo pip install confluent-kafka-python/
echo "Try running your producer now :)"

#Sometimes running 'sudo apt-get purge librdkafka1' helps if the script doesn't work initially...not sure why
