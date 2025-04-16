comfy --skip-prompt --workspace=/var/nfs-mount/comfyUI/ComfyUI install --nvidia
comfy --skip-prompt model download --url https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors --relative-path models/unet --set-civitai-api-token hf_token
comfy --skip-prompt model download --url https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors --relative-path models/clip
comfy --skip-prompt model download --url https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors --relative-path models/clip
comfy --skip-prompt model download --url https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors --relative-path models/clip
comfy --skip-prompt model download --url https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors --relative-path models/vae
comfy --skip-prompt model download --url https://huggingface.co/autismanon/modeldump/resolve/main/dreamshaper_8.safetensors --relative-path models/checkpoints
mkdir -p "/var/nfs-mount/comfyUI/workflows"
