#!/bin/bash


COOKIES="$HOME/.limited/comcast_cookies.txt"
URL="https://customer.comcast.com/MyServices/Internet/?ajax=1"

wget  --load-cookies "$COOKIES" -qO- "$URL" | python parse_comcast.py