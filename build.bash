#!/bin/bash

on_err() {
    ERROR_CODE=$?
    echo "error ${ERROR_CODE}"
    echo "the command executing at the time of the error was"
    echo "${BASH_COMMAND}"
    echo "on line ${BASH_LINENO[0]}"
    exit ${ERROR_CODE}
}
trap on_err ERR

NOW=`date -u +"%Y.%m.%d %H.%M.%S (UTC)"`

HOST_HEADER_LINES=$(grep -c '#.*' hosts.txt)
HOST_HEADER=$(head -${HOST_HEADER_LINES} hosts.txt)
HOST_LIST=$(tail -n +$((${HOST_HEADER_LINES}+1)) hosts.txt | sort -nf | uniq)
REGEX_LIST=()
UBL_LIST=()

echo "${HOST_HEADER}" > hosts.txt

while IFS= read -r line; do 
    if [ -n "$line" ]; then
        line=${line,,}
        echo "$line" >> hosts.txt

        line=$(echo "$line" | sed 's/[\r\n]//g;')

        re=$(echo "$line" | sed 's/\./\\./g; s/\?/./g; s/\-/\\-/g; s/\*/\\w\*/g')
        REGEX_LIST+=($re)

        if [[ $line == *'?'* ]] || [[ $line == *'*'* && $line != '*'* ]]; then
            re="/^.*:\\/\\/$re\\//"
        else
            re="*://$line/*"
        fi

        UBL_LIST+=($re)
    fi
done <<< "$HOST_LIST"

function join { local IFS="$1"; shift; echo "$*"; }

REGEX=$(join '|' ${REGEX_LIST[@]})
UBL=$(join $'\n' ${UBL_LIST[@]})

##################################################

cat <<EOF > only-stackoverflow.txt
[Adblock Plus 2.0]
! 
! Please do not copy this file, Subscribe this filter by clicking the "Subscribe only-stackoverflow filter" button in the middle of the link below.
! 이 파일을 복사하지 말고 아래 링크의 중간에 있는 "추가하기" 버튼을 클릭하여 추가해주세요.
! https://github.com/RyuaNerin/only-stackoverflow
! 
! Title: only-stackoverflow
! Description: Hide copy of stackoverflow from google and duckduckgo search results. (e.g. stackoverrun)
! Homepage: https://github.com/RyuaNerin/only-stackoverflow
! License: https://github.com/RyuaNerin/only-stackoverflow#license
! Expires: 1 hour
! Version: ${NOW}
! 
google.*#?#:is(div#search, div#botstuff) div[data-async-context] div.g[data-hveid]:-abp-contains(/${REGEX}/)
duckduckgo.com#?#div.results article:-abp-contains(/${REGEX}/)
EOF

cat <<EOF > ublacklist.txt
# Please do not copy this file, Subscribe this filter by the link below
# 이 파일을 복사하지 말고 아래 링크를 구독해주세요.
# https://raw.githubusercontent.com/RyuaNerin/only-stackoverflow/master/ublacklist.txt
#
${UBL}
EOF
