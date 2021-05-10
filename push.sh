docker build . -t t1il/covid-bot
docker push t1il/covid-bot
curl -H "Redeploy-Token: bvweiwqjdanfawjKL" 192.168.178.66:9000/hooks/redeploy
26ac0da0-a344-11eb-bcbc-0242ac130002
