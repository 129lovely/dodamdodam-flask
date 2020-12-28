# konly, mecab 설치

```
$ sudo apt-get update
$ sudo apt-get install openjdk-8-jdk python-dev python3-dev
$ java -version
$ sudo pip3 install konlpy jpype1-py3
$ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

libmecab.so.2 링크 생성

```
$ cd /tmp/mecab-0.996-ko-0.9.2
$ ./configure
$ make
$ make check
$ sudo make install

$ cd /tmp/mecab-ko-dic-2.1.1-20180720
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install
```

https://yuddomack.tistory.com/entry/%EC%B2%98%EC%9D%8C%EB%B6%80%ED%84%B0-%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-EC2-konlpy-mecab-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0ubuntu

# 기타 필요한 라이브러리 설치
