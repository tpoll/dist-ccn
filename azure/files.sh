#Argument 1 is ip of node to upload scripts to

scp relay_node.sh $1:~/
scp node_install.sh $1:~/
scp create_start_script.sh $1:~/
scp add_face.sh $1:~/
scp create_content.sh $1:~/
scp server $1:~/

