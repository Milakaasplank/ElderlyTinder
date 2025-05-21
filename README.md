# How to add a simple service
1. Copy the files from lab4 
2. Make a venv in other_Services_tinder
3. install requirements_dev.txt
4. cd to other_services_tinder
5. python app.py
6. Copy past the local host link to insomnia
7. Go to insomnia and make a new POST request
8. Add a json body, and come up with the necessary data
9. Click send.

## Deploy it to a VM
1. Make a VM with settings: ubuntu 24.04 lts, E2 (4 core )

According to aurelia, copy paste in equivalent code when making a vm'
gcloud compute instances create instance-20250509-131419 \
    --project=mythical-lens-450121-n0 \
    --zone=us-central1-c \
    --machine-type=e2-standard-4 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata=enable-osconfig=TRUE \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=mythical-lens-450121-n0@appspot.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=instance-20250509-131419,disk-resource-policy=projects/mythical-lens-450121-n0/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/ubuntu-os-cloud/global/images/ubuntu-minimal-2404-noble-amd64-v20250501,mode=rw,size=10,type=pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ops-agent-policy=v2-x86-template-1-4-0,goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
&& \
printf 'agentsRule:\n  packageState: installed\n  version: latest\ninstanceFilter:\n  inclusionLabels:\n  - labels:\n      goog-ops-agent-policy: v2-x86-template-1-4-0\n' > config.yaml \
&& \
gcloud compute instances ops-agents policies create goog-ops-agent-v2-x86-template-1-4-0-us-central1-c \
    --project=mythical-lens-450121-n0 \
    --zone=us-central1-c \
    --file=config.yaml

2. sudo apt install git
3. git clone https://github.com/Milakaasplank/ElderlyTinder
4. cd ElderlyTinder/installation_script
5. sh docker.sh
6. sh docker_compose.sh
7. gcloud compute firewall-rules create flask-port-1 --allow tcp:5000
gcloud compute firewall-rules create flask-port-2 --allow tcp:5001
8. cd ..
9. cd other_services_tinder

10. sudo docker build -t elderlytinder:0.0.1 .
10. sudo docker build -t caregiver:0.0.1 .
10. sudo docker build -t elderly:0.0.1 .


11. sudo docker run -p 5000:5000 -d --name=elderlytinder elderlytinder:0.0.1
11. sudo docker run -p 5000:5000 -d --name=caregiver caregiver:0.0.1
11. sudo docker run -p 5000:5000 -d --name=elderly elderly:0.0.1


12. sudo docker start elderlytinder
12. sudo docker start caregiver
12. sudo docker start elderly