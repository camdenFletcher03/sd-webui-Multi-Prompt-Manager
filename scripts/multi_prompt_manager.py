import contextlib
import gradio as gr
from modules import scripts
import json
import os

# Shoutout to https://github.com/EnsignMK/ExampleSendText for giving an example of how to send input to the main prompt :)

PROMPTS_FILE = "prompts.json"


def copy_from_active_prompt(is_negative, pos_prompt, neg_prompt):
    if is_negative:
        return neg_prompt
    return pos_prompt


class MultiPromptManager(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    def title(self):
        return "Multi-Prompt Manager"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        # Load existing prompts
        if os.path.exists(PROMPTS_FILE):
            with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
        else:
            prompts = {}

        def load_prompt(selected_prompt):
            prompt_data = prompts.get(selected_prompt, {"prompt": "", "is_negative": False})
            return prompt_data['prompt'], prompt_data['is_negative']

        def save_prompt(new_name, new_prompt, is_negative):
            if not new_name:
                existing_names = set(prompts.keys())
                i = 1
                while f"prompt {i}" in existing_names:
                    i += 1
                new_name = f"prompt {i}"

            prompts[new_name] = {'prompt': new_prompt, 'is_negative': is_negative}
            with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(prompts, f)
            return gr.Dropdown.update(choices=list(prompts.keys())), ""

        def delete_prompt(selected_prompt):
            if selected_prompt in prompts:
                del prompts[selected_prompt]
                with open(PROMPTS_FILE, 'w') as f:
                    json.dump(prompts, f)
                return gr.Dropdown.update(choices=list(prompts.keys())), "", ""
            return gr.Dropdown.update(), "", ""

        def use_prompt(new_prompt, is_negative):
            if not is_negative:
                return gr.update(value=new_prompt), gr.update()
            return gr.update(), gr.update(value=new_prompt)
        
        with gr.Group():
            with gr.Accordion("Multi-Prompt Manager", open=False):
                with gr.Row():
                    prompt_dropdown = gr.Dropdown(choices=list(prompts.keys()), label="Select Prompt")
                    new_prompt_name = gr.Textbox(label="Enter Prompt Name", tooltip="Give this prompt a cool and memorable name.")

                use_prompt_button = gr.Button("Use Prompt", variant="primary", elem_id="use-prompt-button", tooltip="Replace whatever text is currently in the active prompt field with the selected prompt.")
                prompt_input = gr.Textbox(label="Prompt", lines=5)
                negative_prompt_toggle = gr.Checkbox(label="This is a Negative Prompt", value=False, tooltip="Whether or not this should be sent over to the negative prompt field.")
                
                with gr.Row():
                    save_button = gr.Button("Save Prompt", tooltip="Save the prompt to your prompts list.")
                    delete_button = gr.Button("Delete Prompt", tooltip="Remove the prompt from your prompts list.")
                    copy_prompt_button = gr.Button("Copy from Active Prompt", tooltip="Copy over the prompt from the active prompt field into Multi-Prompt Manager.")

                with contextlib.suppress(AttributeError):
                    prompt_dropdown.change(fn=load_prompt, inputs=[prompt_dropdown], outputs=[prompt_input, negative_prompt_toggle])
                    save_button.click(fn=save_prompt, inputs=[new_prompt_name, prompt_input, negative_prompt_toggle], outputs=[prompt_dropdown, new_prompt_name])
                    delete_button.click(fn=delete_prompt, inputs=[prompt_dropdown], outputs=[prompt_dropdown, prompt_input, new_prompt_name])

                    if is_img2img:
                        use_prompt_button.click(fn=use_prompt, inputs=[prompt_input, negative_prompt_toggle], outputs=[self.boxxIMG, self.neg_boxxIMG])
                        copy_prompt_button.click(fn=copy_from_active_prompt, inputs=[negative_prompt_toggle, self.boxxIMG, self.neg_boxxIMG], outputs=[prompt_input])
                    else:
                        use_prompt_button.click(fn=use_prompt, inputs=[prompt_input, negative_prompt_toggle], outputs=[self.boxx, self.neg_boxx])
                        copy_prompt_button.click(fn=copy_from_active_prompt, inputs=[negative_prompt_toggle, self.boxx, self.neg_boxx], outputs=[prompt_input])

        return [prompt_dropdown, use_prompt_button, save_button, delete_button, copy_prompt_button, new_prompt_name, prompt_input, negative_prompt_toggle]
    
    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":
            self.boxx = component
        if kwargs.get("elem_id") == "img2img_prompt":
            self.boxxIMG = component
        if kwargs.get("elem_id") == "txt2img_neg_prompt":
            self.neg_boxx = component
        if kwargs.get("elem_id") == "img2img_neg_prompt":
            self.neg_boxxIMG = component


print("Successfully loaded Multi-Prompt Manager extension.")
