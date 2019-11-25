# How to setup MLflow on Virtual Machine 

## 1. Create a VM on azure with the following specifications:
Microsoft Datacenter 2019: B2ms, Standard, General purpose, CPU 2, RAM 8, Datadisks 4, Max Iops 1920, Temp. Storage 16
- Allow acces to HTTP, HTTPS, SSH and RDP when creating the VM
- Remember username and password used for server, you'll need these credentials later

## 2. Connect to the VM by Starting Microsoft Remote Desktop (you can download this software on mac)
- Add PC: hostname: Public IP-Adress VM : RDP Port (example: 52.137.9.17:3389)
- Connect to server (username and password are those used when creating the server)

## 3. Once connection is done and you're on de Desktop of the server do the following:
- install python: go to internet explorer https://www.python.org/downloads/release/
- open up command line in server and type the following to install pip: 
```	> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
```> python get-pip.py```
- install mlflow using pip
```> pip install mlflow```

- start mlflow server on VM
```> mlflow server host 0.0.0.0```

!mlflow server is now running on port 5000 on your VM.

## 4. Adjust firewall settings on VM
- Navigate to the following directory: Control Panel\System and Security\Windows Defender Firewall
- Go to Advanced Settings -> Inbound Rules
- Add new Inbound Rule: Port -> TCP -> specific local ports: 5000 (or all) -> ... 

## 5. Go to Azure VM portal and add a Inbound port
- Add inbound port rule and use port 5000. Allow access 'any'

## 6. Check wether you can access the MLflow UI
Go to 'http://Public IP-Adress VM/5000' (example: http://52.137.9.17:5000/) url in your browser. 





