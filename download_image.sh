for a b in $(cat ../imagenet.synset.geturls.getmapping.txt); do
    wget -nv $(echo $b |tr -d '\r') -O $a
done
