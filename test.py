- name: List Docker containers
      run: docker container ls -a
 
   - name: Stop and remove Docker containers
      run: |
        docker stop $(docker ps -aq)
        docker rm $(docker ps -aq)    
 
   - name: List Docker images
      run: docker image ls
 
    - name: Delete Docker images
      run: |
        docker rmi -f $(docker images -aq)
    - name: List Docker images after deletion
      run: docker image ls
