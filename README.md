dlib で靴の検出器作成
===

TreeView: http://image-net.org/synset?wnid=n13926786#

```
$ # mapping を取得
$ curl -L http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid=n13926786
$
$ # 画像を取得
$ mkdir images
$ for a b in $(cat ../mapping.txt); do
    wget -nv $(echo $b |tr -d '\r') -O images/$a.jpg
  done
$
$ # Bounding Boxes を取得
$ # curl -L "http://www.image-net.org/api/download/imagenet.bbox.synset?wnid=n13926786" > bbox.tar.gz
$ # なぜか取ってきてくれないのでリダイレクト先を直接取得
$ curl -L "http://www.image-net.org/downloads/bbox/bbox/n13926786.tar.gz" > bbox.tar.gz
$
$ # 展開
$ tar zxvf bbox.tar.gz
$
$ ls
Annotation/
bbox.tar.gz
images/
mapping.txt

```
