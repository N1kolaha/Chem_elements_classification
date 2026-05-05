docker run --name my-postgres \
-e POSTGRES_PASSWORD=admin \
-e POSTGRES_DB=kursdb \
-p 5432:5432 -d postgres

docker exec -it my-postgres psql -h localhost -U postgres -d kursdb -f kursdb.sql
