#!/bin/bash

if [ $(id -u) -ne 0 ] ; then
	echo "❌ Run me as root"
	exit 1
fi

DNF=$(which dnf)
APT=$(which apt)

if [ ! -z $DNF ] ; then
	dnf install -y haproxy
elif [ ! -z $APT ] ; then
	apt install -y haproxy
fi

cp haproxy.cfg /etc/haproxy
sed -i "s/8080/80/" /etc/haproxy/haproxy.cfg
systemctl stop haproxy
systemctl start haproxy

echo "hello" > /opt/bunkerweb/www/index.html