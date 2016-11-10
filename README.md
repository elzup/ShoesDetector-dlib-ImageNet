dlib で靴の検出器作成
===

TreeView: http://image-net.org/synset?wnid=n13926786#

## 準備


mapping ファイルを取得

```sh
$ curl -L http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid=n13926786 > mapping.txt
```


画像を取得。images/ 下に保存

```sh
$ mkdir images
$ for a b in $(cat mapping.txt); do
    wget -T1 -nv $(echo $b |tr -d '\r') -O images/$a.jpg
  done
$ # 空の画像ファイル削除
$ find images -empty -delete
```

flickr などの白い not available な画像を削除

Bounding Boxes を取得

``

```sh
$ # curl -L "http://www.image-net.org/api/download/imagenet.bbox.synset?wnid=n13926786" > bbox.tar.gz
$ # なぜか取ってきてくれないのでリダイレクト先を直接取得
$ curl -L "http://www.image-net.org/downloads/bbox/bbox/n13926786.tar.gz" > bbox.tar.gz
$
$ # 展開
$ tar zxvf bbox.tar.gz
```


ディレクトリ内容確認

```
$ ls
Annotation/
bbox.tar.gz
images/
mapping.txt
```
