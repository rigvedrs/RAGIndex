# To Build images
docker build -t doc-qna .

# To Run Container
docker run -d -p 8000:8501 --name doc-qna doc-qna
