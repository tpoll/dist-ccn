#Argument 1 is ip of node to upload scripts to

scp relay_node.sh $1:/home/todd
scp node_install.sh $1:/home/todd
scp create_start_script.sh $1:/home/todd
scp add_face.sh $1:/home/todd
scp create_content.sh $1:/home/todd
scp server $1:/home/todd

