import subprocess
import os
import uuid
from comfy_utils import start_comfyui_background, check_comfyui, load_workflow, prompt_update_workflow, send_comfyui_request, get_img_file_path, image_to_base64

class InferlessPythonModel:
    def initialize(self):
        self.directory_path = "/opt/tritonserver"
        
        if not os.path.exists(self.directory_path+"/ComfyUI"):
            subprocess.run(["wget", "https://github.com/rbgo404/ComfyUI-inferless-template/raw/main/build.sh"])
            subprocess.run(["bash", "build.sh"], check=True)
        
        self._data_dir = self.directory_path+"/workflows"
        self.server_address = "127.0.0.1:8188"
        self.client_id = str(uuid.uuid4())
        
        start_comfyui_background()
        self.ws = check_comfyui(self.server_address,self.client_id)

    def infer(self, inputs):
        workflow_name = inputs.get("workflow_name")
        prompt = inputs.get("prompt")
        workflow = load_workflow(self.directory_path,workflow_name)
        prompt = prompt_update_workflow(workflow_name,workflow,prompt)
        try:
            prompt_id = send_comfyui_request(self.ws, prompt, self.server_address,self.client_id)
            file_path = get_img_file_path(self.server_address,prompt_id)
            image_base64 = image_to_base64(file_path)
        
        except Exception as e:
            print("Error occurred while running Comfy workflow: ", e)

        return {"generated_image_base64":image_base64}
    
    def finalize(self):
        pass
