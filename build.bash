#!/bin/bash

NOW=`date -u +"%Y.%m.%d %H.%M.%S (UTC)"`

HOST_LIST=`cat hosts.txt | sort -n | uniq`
REGEX_LIST=()

truncate hosts.txt -s 0

while IFS= read -r line; do 
	if [ -n "$line" ]; then
		echo "$line" >> hosts.txt

		re=$(echo "$line" | sed 's/\./\\./g; s/\-/\\-/g; s/\*/.\*/g')
        echo $re

		REGEX_LIST+=($re)
	fi
done <<< "$HOST_LIST"

function join { local IFS="$1"; shift; echo "$*"; }

REGEX=$(join '|' ${REGEX_LIST[@]})

##################################################

cat <<EOF > only-stackoverflow.txt
[Adblock Plus 2.0]
! Title: only-stackoverflow
! Description: Hide copy of stackoverflow from google and duckduckgo search results. (e.g. stackoverrun)
! Homepage: https://github.com/RyuaNerin/only-stackoverflow
! License: https://github.com/RyuaNerin/only-stackoverflow#license
! Expires: 1 days
! Version: ${NOW}

google.com#?#div[role=\"main\"] div#search div[data-async-context] div[data-ved]:-abp-contains(/${REGEX}/)
google.co.kr#?#div[role=\"main\"] div#search div[data-async-context] div[data-ved]:-abp-contains(/${REGEX}/)
duckduckgo.com#?#div.result:-abp-contains(/${REGEX}/)
EOF
