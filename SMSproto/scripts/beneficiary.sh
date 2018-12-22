#!/usr/bin/bash

curl -H "Content-Type: application/json" -X POST -d '{
	"sign": "0x8bb956201d00f208599de2cd9ae1ed1032df52a02bd62ee0c127f8514fc364270b93d1ee5e80ed73740b6eaf1a88d293615aa936ac09208523d3a5f0e8c2cfa600",
	"secret": "abcde"
}' http://localhost:5000/account/0x9a43BB008b7A657e1936ebf5d8e28e5c5E021596
