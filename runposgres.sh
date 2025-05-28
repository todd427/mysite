docker run --name=blog_db -e POSGRES_DB=blog-e POSTGRES_USER=blog-e POSTGRES_PASSWORD=totme -p 5432:5432 -d postgres:16.2
