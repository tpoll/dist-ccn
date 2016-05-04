#!/bin/bash
#Add ccn node to startup scripts
cat <<EOF >  /etc/init.d/serverStart
#!/bin/sh
cd /home/todd
./server > slog.txt &
EOF
chmod ugo+x /etc/init.d/serverStart
update-rc.d serverStart defaults