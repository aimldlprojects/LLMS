deploy:
    needs: build
    runs-on: self-hosted
    steps:
      - name: Pull UI Docker image
        env:
          ECR_REGISTRY: ***add ecr registry name***
          ECR_REPOSITORY: ***add ecr repository name***
          IMAGE_TAG: ${{ github.sha }}    
        run: |
          docker pull $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "UI Docker image is pulled from $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
 
      - name: Delete Old docker container
        run: |
          docker rm -f ***add a container name*** || true
          echo "Deleted old UI container"
 
      - name: Run Docker Container
        run: |
          sudo docker run -d -p 3015:80 --name ***add a container name*** $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "Running UI container"
     
      - name: Pull App Docker image
        env:
          ECR_REGISTRY: ***add ecr registry name***
          ECR_REPOSITORY: ***add ecr repository name***
          IMAGE_TAG: ${{ github.sha }}    
        run: |
          docker pull $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "App Docker image is pulled from $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
 
      - name: Delete Old docker container
        run: |
          docker rm -f ***add a container name*** || true
          echo "Deleted old App container"
 
      - name: Run Docker Container
        run: |
          sudo docker run -d --name ***add a container name*** -p 8015:8015  $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "Running App2 container"
