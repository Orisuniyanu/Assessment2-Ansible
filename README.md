# Flask App Deployment with Ansible and Nginx Load Balancer

This project automates the deployment of multiple Flask-based container applications on a remote Docker host using **Ansible**. It also configures an **NGINX Load Balancer** to distribute traffic across the containers.

---

## 📦 Project Structure

.
├── inventory.sample.yaml # Sample inventory (copy and edit this)
├── playbook.yml # Main Ansible playbook
├── roles
│ ├── appdeploy # Role to manage Flask containers
│ │ └── tasks
│ │ └── main.yml
│ └── loadbalancer # Role to configure Nginx
│ ├── tasks
│ │ └── main.yml
│ └── templates
│ └── nginx.conf.j2
└── website-flask # Flask app source code
├── app.py
├── static/
└── templates/

---

## 🚀 What It Does

- Builds and runs 5 Ubuntu-based containers with Flask.
- Deploys your website code inside each container.
- Installs `Flask` and `requests` in each container.
- Sets up a load balancer (NGINX) to route requests evenly.
- Shows which container handled the request and checks other containers' status.
- Provides a sample inventory file for easy configuration.

## 🛠️ Requirements

- Ansible
- Docker
- NGINX
- Flask
- Python 3.x

- Control Node with:
  - Python3 and Ansible installed.
- Two remote Linux servers:
  1. **Docker Host**: Where the 5 containers will run.
  2. **Load Balancer Host**: Where NGINX will run.

- SSH access from Control Node to both remote machines.
- Docker installed on the Docker Host.


## 📋 Usage

1. Update the `inventory.yaml` file with your server details.
2. Run the Ansible playbook:

```bash
ansible-playbook -i inventory.yaml playbook.yml
```

3. Access the load balancer at `http://<load_balancer_ip>/` to see your Flask apps in action.
4. Check the status of each container by accessing `http://<load_balancer_ip>/status`.
5. To stop the containers, run:
```bash
ansible-playbook -i inventory.yaml playbook.yml --tags stop
```
 