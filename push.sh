docker build . -t t1il/covid-bot
docker push t1il/covid-bot
curl -H "Redeploy-Token: bvweiwqjdanfawjKL" jkoenig.dev:9000/hooks/redeploy-devmarkt
