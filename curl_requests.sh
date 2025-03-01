curl -X GET "http://localhost:3000/api/v1/analysis/" \
     -H "Content-Type: application/json" \
     -d '{"uri": "./example_imgs/image1.png"}'