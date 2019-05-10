#!/bin/bash

LOGIN_URL=http://localhost:8080/admin/login/
COOKIES=cookies.txt

CURL_BIN="curl --silent --cookie $COOKIES --referer $LOGIN_URL"

if [ ! -f $COOKIES ]
then
    echo "Django Auth:"
    echo -n " get csrftoken ..."
    $CURL_BIN --cookie-jar $COOKIES $LOGIN_URL > /dev/null
    DJANGO_TOKEN="csrfmiddlewaretoken=$(sed -n -e 's/^.*csrftoken[[:blank:]]*//p' $COOKIES)"
    echo

    YOUR_USER='mario'
    YOUR_PASS='xxxxxxxxxxxxxxxx'
    echo -n " perform login ..."
    $CURL_BIN --cookie-jar $COOKIES \
        --data "$DJANGO_TOKEN&username=$YOUR_USER&password=$YOUR_PASS" \
        --request POST $LOGIN_URL
    DJANGO_TOKEN="csrfmiddlewaretoken=$(sed -n -e 's/^.*csrftoken[[:blank:]]*//p' $COOKIES)"
    echo
    echo "Authenticated"
fi

echo -n " all accessions: "
$CURL_BIN \
    --data "$DJANGO_TOKEN" \
    --request GET http://localhost:8080/collection/accessions/
echo
echo -n " all plants for accession 2014.0002: "
$CURL_BIN \
    --data "$DJANGO_TOKEN" \
    --request GET http://localhost:8080/garden/accessions/2014.0002/plants/
echo
#echo "remove cookies file to logout"
#rm $COOKIES
