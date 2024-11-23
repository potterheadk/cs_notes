## ⚠️ **Some Images are Ai generated so be careful :)**  ⚠️

![[topics.png]]



![[user_diagram.webp]]


![[kubernetics_overview.webp]]



Kubernetes is an open-source container orchestration platform designed to automate the deployment, scaling, and management of containerized applications. Here’s a breakdown of its key features and uses:

### What is Kubernetes?

- **Container Orchestration**: Kubernetes manages clusters of containers, which are lightweight, portable units that package an application and its dependencies.
- **Open-Source**: Developed by Google, it is now maintained by the Cloud Native Computing Foundation (CNCF).
- **API Driven**: Kubernetes uses a REST API for all its interactions, allowing for easy integration with other tools and services.

### Key Features

- **Automated Deployment**: Kubernetes can automatically deploy and roll out changes to applications with minimal downtime.
- **Scaling**: It can scale applications up or down based on demand, automatically adjusting the number of running containers.
- **Load Balancing**: Kubernetes provides built-in load balancing to distribute traffic evenly across containers, improving application performance and reliability.
- **Self-Healing**: If a container fails, Kubernetes can automatically restart or replace it to maintain the desired state of the application.
- **Service Discovery and Networking**: Kubernetes can expose containers using DNS names or IP addresses, enabling easy communication between services.
- **Storage Orchestration**: It can automatically mount the storage system of your choice, such as local storage, public cloud providers, or network storage.

### Common Use Cases

- **Microservices Architecture**: Kubernetes is often used to manage microservices, allowing teams to develop and deploy services independently.
- **Hybrid and Multi-Cloud Deployments**: Organizations can use Kubernetes to manage applications that span multiple cloud providers or on-premises environments.
- **CI/CD Pipelines**: It integrates well with Continuous Integration and Continuous Deployment workflows, automating application updates and testing.
- **Development and Testing**: Developers can use Kubernetes to create isolated environments for testing applications without affecting production systems.

### Conclusion

Kubernetes is a powerful tool for organizations looking to leverage containerization to improve their application deployment and management processes, making it easier to manage complex applications at scale.

-----------------------------------
## what is Microservices,Orchestration,CI/CD
### Microservices

- **Definition**: Microservices is an architectural style where an application is composed of small, independent services that communicate over a network. Each service is responsible for a specific business function and can be developed, deployed, and scaled independently.
    
- **Characteristics**:
    
    - **Independence**: Each microservice can be developed and deployed independently, without affecting the entire application.
    - **Loose Coupling**: Services interact through well-defined APIs, reducing dependencies between them.
    - **Resilience**: Failure in one service doesn't necessarily mean the whole system fails. Other services can continue to operate.
    - **Scalability**: Each service can be scaled individually based on its load, rather than scaling the entire application.
- **Use Case**: For example, an e-commerce platform could have separate microservices for handling user authentication, product catalog, shopping cart, and payment processing. Each of these services can be managed, updated, and scaled independently.
    

### Orchestration

- **Definition**: Orchestration refers to the automated configuration, coordination, and management of complex computer systems, middleware, and services. In the context of microservices, orchestration involves managing the deployment, scaling, networking, and lifecycle of services within an application.
    
- **Kubernetes as an Example**: Kubernetes is a popular tool used for orchestrating containers in a microservices architecture. It automates tasks like deploying new versions of services, scaling services up or down, and managing the underlying infrastructure.
    
- **Benefits**:
    
    - **Automation**: Reduces manual intervention by automating repetitive tasks.
    - **Consistency**: Ensures consistent deployment and management practices across different environments (development, testing, production).
    - **Complexity Management**: Simplifies the management of complex, distributed applications.

### CI/CD (Continuous Integration/Continuous Deployment)

- **Definition**: CI/CD is a set of practices that aim to automate the integration and deployment of code changes, ensuring faster and more reliable software delivery.
    
- **Continuous Integration (CI)**:
    
    - Developers frequently merge code changes into a shared repository.
    - Automated tests are run to detect any issues early in the development process.
    - Ensures that the codebase is always in a deployable state.
- **Continuous Deployment (CD)**:
    
    - Automates the process of deploying code changes to production or other environments.
    - After code passes automated tests, it can be automatically deployed to production without manual intervention.
    - Reduces the time it takes to deliver new features and fixes to users.
- **Benefits**:
    
    - **Faster Time to Market**: Automates the testing and deployment process, speeding up the release cycle.
    - **Improved Quality**: Automated tests catch bugs early, reducing the risk of issues in production.
    - **Lower Risk**: Smaller, more frequent releases reduce the risk associated with big-bang deployments.
- **Tools**: Jenkins, GitLab CI, Travis CI, CircleCI, and GitHub Actions are some of the popular tools used to implement CI/CD pipelines.
    

### Summary

- **Microservices**: Breaks down an application into small, independent services that can be developed, deployed, and scaled separately.
- **Orchestration**: Automates the management of complex systems and services, especially in a microservices architecture.
- **CI/CD**: A set of practices that automate the integration and deployment of code changes, enabling faster and more reliable software delivery.


------------------------
# Master and worker  Basic Architecture :

### Each worker node we call it kubelet (primary"node agent")

![[master_worker.png]]


------------------
# What is actually happening inside master node: 

![[master_node.png]]

---------------------------------

# Inside Each Worker Node :  (can do static IP using service)

# 2 types of services : 

------------------------------------------------------------------------
### **Internal Services**

##### Internal services are used for communication between different applications or components within the Kubernetes cluster. These services are not exposed to the outside world.
#### **ClusterIP** (default service type): This type of service exposes the application on a cluster-internal IP. Only applications within the cluster can access this service. It's typically used for internal communication between microservices or components of an application.
------------------------------------------------------------------------

### **External Services**

##### External services are used to expose applications running in a Kubernetes cluster to the outside world, allowing external users or systems to interact with the application.

#####  **NodePort**: This type of service exposes the application on a specific port on each node in the cluster. The service can be accessed externally by sending requests to the node's IP address and the specified port.

##### **LoadBalancer**: This service type creates an external load balancer (often provided by the cloud provider) that automatically routes traffic to the application. It exposes the application to the internet by provisioning a public IP address.

##### **Ingress**: Ingress is not a service type but a resource that manages external access to services in a Kubernetes cluster, typically HTTP/HTTPS. It allows for more complex routing rules, such as load balancing, SSL termination, and path-based routing.
------------------------------------------------------------------------


![[worker_node.png]]


------------------------
## External configuration 

In Kubernetes, **ConfigMaps** and **Secrets** are used to externalize configuration data from the application code. This allows you to manage configuration separately and securely, making applications more portable and easier to manage across different environments.

### **ConfigMaps**

A ConfigMap is an API object that allows you to store non-sensitive configuration data in key-value pairs. It can be used to inject configuration data into your pods as environment variables, command-line arguments, or configuration files.

#### **Use Cases**

- Storing configuration data that your application might need, such as database URLs, service endpoints, or feature flags.
- Managing configuration for multiple environments (e.g., development, testing, production) without changing the application code.

-------------------------------------------------------------------

### **Secrets**

A Secret is an API object that stores sensitive data, such as passwords, OAuth tokens, or SSH keys. Secrets are similar to ConfigMaps but are specifically designed to handle sensitive information, providing more security through base64 encoding and the ability to restrict access.

#### **Use Cases**

- Storing sensitive data like database passwords, API keys, or TLS certificates.
- Managing access to sensitive configuration separately from other, non-sensitive configuration data.
------------------------

# #Volumes

![[volumes.png]]




# Basic visualization : of fundamental stuff 

![[fundamental_overview.webp]]




# #Minikube-and-kubectl


# #Production-cluster-setup-Overview : 

![[production_cluster_overview.png]]


# #minikube_local_cluster_overview :

![[minikube_local_cluster.png]]


# #What_is_kubectl :

![[what_is_kubectl.png]]


# #kubectl_minikube + :

![[kubectl+minikube.png]]



* # kubectl is dependency of minikube most 


* # Kubernetes, **Deployments** are a higher-level abstraction used to manage and maintain **Pods**. While you can directly create Pods, it's more common to create Deployments because they provide additional functionality like:

- **Scaling:** Automatically scaling the number of Pods up or down.
- **Self-healing:** Automatically replacing Pods that fail or are terminated.
- **Rolling Updates:** Updating Pods incrementally without downtime.

When you create a Deployment, it automatically manages the creation and maintenance of Pods for you. So while you typically work with Deployments, it is the Deployment that actually creates and manages the Pods.

* ##  Following are some commands to help get you started 

~~~
# installation on archlinux
sudo pacman -S minikube kubectl 
# check kubectl version client/server version  

minikube status # gives current running status of containers

# how to get web dashboard
minikube dashboard --url --port=0 # port 0 for random port choosed

# kubectl 
kubectl get nodes # give current running status of nodes
kubectl get pods # running status of pods
kubectl get services # Active services

# kubernetics debugging basic level 
kubectl exec -it <pod_name> -- /bin/bash # for debugging purpose
kubectl logs <pod_name_id>  # get logs of that image
kubectl describe pod <pod_name> # detailed description for that pod

# creating deployments

kubectl create deployment <pod_name_you_want> --image=nginx(or image you want)


# how to apply config file 
kubectl apply -f [filename]  #config.yaml (for ex)



~~~
