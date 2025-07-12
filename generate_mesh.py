import torch
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images
from shap_e.util.notebooks import decode_latent_mesh
import os

def generate_shapes(prompt_list, output_dir="outputs", render_mode="nerf", size=128):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    os.makedirs(output_dir, exist_ok=True)

    print(f"Using device: {device}")
    print(f"Generating for prompts: {prompt_list}")

    xm = load_model('transmitter', device=device)
    model = load_model('text300M', device=device)
    diffusion = diffusion_from_config(load_config('diffusion'))

    latents = sample_latents(
        batch_size=len(prompt_list),
        model=model,
        diffusion=diffusion,
        guidance_scale=12.0,
        model_kwargs=dict(texts=prompt_list),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=5,
    )

    print("Decoding and saving meshes...")
    for i, latent in enumerate(latents):
        mesh = decode_latent_mesh(xm, latent).tri_mesh()
        out_path = os.path.join(output_dir, f"mesh_{i}.obj")
        with open(out_path, 'w') as f:
            mesh.write_obj(f)
        print(f"Saved: {out_path}")

    print("Done.")

if __name__ == "__main__":
    prompts = ["one shark"]
    generate_shapes(prompts)
