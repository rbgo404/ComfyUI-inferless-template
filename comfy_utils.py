import json
import urllib.request
import urllib.error
import logging
import time
import subprocess
import os
import websocket
import threading
import sys
import base64

logging.basicConfig(level=logging.DEBUG)
# Change volume here
COMFYUI_DIR = "/var/nfs-mount/ComfyUI-VOL-latest/ComfyUI"

def start_comfyui_background():
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=COMFYUI_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for a short time to see if the process starts successfully
        time.sleep(5)
        
        if process.poll() is None:
            logging.info("ComfyUI server process started successfully.")
            return process
        else:
            stdout, stderr = process.communicate()
            logging.error(f"ComfyUI server failed to start. Stdout: {stdout}, Stderr: {stderr}")
            raise Exception("ComfyUI server failed to start")
    except Exception as e:
        logging.error("Failed to run setup_comfyui:", exc_info=True)
        raise Exception("Error setting up ComfyUI repo") from e

def run_comfyui_in_background():
    def run_server():
        process = start_comfyui()
        if process:
            stdout, stderr = process.communicate()

    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    logging.info("ComfyUI server thread started")

def check_comfyui(server_address,client_id):
    socket_connected = False
    while not socket_connected:
        try:
            ws = websocket.WebSocket()
            ws.connect(
                "ws://{}/ws?clientId={}".format(server_address, client_id)
            )
            socket_connected = True
        except Exception as e:
            print("Could not connect to comfyUI server. Trying again...")
            time.sleep(5)
    print("Successfully connected to the ComfyUI server!")
    return ws

def load_workflow(directory_path,workflow_name):
    with open(f"{directory_path}/workflows/{workflow_name}.json", 'rb') as file:
        return json.load(file)

def prompt_update_workflow(workflow_name,workflow,prompt):
    if workflow_name == "flux_workflow":
        workflow["6"]["inputs"]["text"] = prompt
        return workflow
    
def send_comfyui_request(ws, prompt, server_address,client_id):
    p = {"prompt": prompt,"client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    url = f"http://{server_address}/prompt"
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    logging.debug(f"Sending request to: {url}")
    logging.debug(f"Request data: {data.decode('utf-8')}")

    with urllib.request.urlopen(req, timeout=10) as response:
        response = json.loads(response.read())
    
    while True:
        prompt_id = response["prompt_id"]
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            print(message)
            if message["type"] == "executing":
                data = message["data"]
                if data["node"] is None and data["prompt_id"] == prompt_id:
                    break
        else:
            continue
    return prompt_id

def get_img_file_path(server_address,prompt_id):
    with urllib.request.urlopen(
        "http://{}/history/{}".format(server_address, prompt_id),timeout=10
    ) as response:
        output = json.loads(response.read())
        print(output)

    print(output)
    outputs = output[prompt_id]["outputs"]
    for node_id in outputs:
        node_output = outputs[node_id]
        print(node_output)
    
    if "images" in node_output:
        image_outputs = []
        for image in node_output["images"]:
                image_outputs.append({"filename": image.get("filename")})
    
    for node_id in image_outputs:
        file_path = f"{COMFYUI_DIR}/output/{node_id.get('filename')}"
    
    return file_path

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')
