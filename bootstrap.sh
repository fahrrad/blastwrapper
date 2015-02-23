#!/usr/bin/env bash

# adding local mirrors 
echo "deb mirror://mirrors.ubuntu.com/mirrors.txt precise main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt precise-updates main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt precise-backports main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt precise-security main restricted universe multiverse" > mirrors.list

sudo cat mirrors.list /etc/apt/sources.list > /etc/apt/sources.list

sudo apt-get update
sudo apt-get install -y ncbi-blast+ rabbitmq-server python3

# Create virtualenv for executing loaders

# Getting test genome
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/drosoph.nt.gz
gunzip drosoph.nt.gz

export BLASTDB=/data/blastdb
echo "export BLASTDB=/data/blastdb" >> ~/.bashrc

sudo mkdir -p /data/blastdb/drosoph
sudo mv drosoph.nt /data/blastdb/drosoph

cd $BLASTDB/drosoph
echo "Creating sampleblast database, based on genome of fruitfly"
sudo makeblastdb -in drosoph.nt -dbtype nucl -out sample_db

