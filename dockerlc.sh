docker run --name=blog_db -e posgres_db=blog-e posgres_user=blog-e postgres_password=totme -p 5432:5432 -d postgres:16.2
