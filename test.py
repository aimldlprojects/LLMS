To replicate the same environment you described, where the Docker CLI is using **Podman** in RHEL 9, you would follow these steps to install and configure **Podman** and alias it to Docker.

### Steps to Set Up Docker CLI with Podman in RHEL 9:

1. **Update the system**:
   Start by ensuring your RHEL 9 system is updated.
   ```bash
   sudo dnf update -y
   ```

2. **Install Podman**:
   RHEL 9 comes with **Podman** available in the default repositories, so install it using `dnf`.
   ```bash
   sudo dnf install -y podman
   ```

3. **Verify Podman installation**:
   After installation, verify that Podman is installed by checking its version.
   ```bash
   podman --version
   ```

4. **Configure Docker CLI to use Podman**:
   In RHEL 9, the Docker CLI is often aliased to Podman by default. You can confirm this by running the following command:
   ```bash
   docker --version
   ```
   If it shows something like "Docker CLI using Podman" or returns the Podman version, you are all set. Otherwise, you can create the alias manually.

5. **Create a Docker alias (if needed)**:
   If Docker is not already aliased to Podman, you can create the alias manually by adding this to your shell configuration file (`~/.bashrc` or `~/.bash_profile`):
   ```bash
   echo 'alias docker=podman' >> ~/.bashrc
   source ~/.bashrc
   ```

6. **Configure rootless Podman (optional)**:
   If you want to run containers without root privileges (rootless containers), configure Podman to support it:
   ```bash
   sudo dnf install -y fuse-overlayfs
   ```

7. **Start Podman**:
   Podman does not require a daemon, so you don't need to start it like Docker. However, you can verify it’s working by running:
   ```bash
   podman info
   ```

8. **Run Docker/Podman commands**:
   You can now use the **Docker CLI** commands (`docker run`, `docker build`, etc.) and they will work with **Podman** as the container engine.

### Additional Optional Steps:

- **Install `podman-compose`**: If you need Docker Compose functionality, you can use `podman-compose`, which is an alternative to `docker-compose`.
  ```bash
  sudo dnf install -y podman-compose
  ```

- **Set up container networking**: If your application requires advanced networking (like Docker's bridge networking), Podman supports it but may require additional setup.

### Summary:
By installing **Podman** and configuring the Docker alias to use Podman, you'll replicate the environment where the Docker CLI works with Podman in RHEL 9.
