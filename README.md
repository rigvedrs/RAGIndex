# To Build images
docker build -t doc-qna .

# To Run Container for vector store
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest


# To Run Container for docqna
docker run -d -p 8000:8501 --name doc-qna doc-qna
