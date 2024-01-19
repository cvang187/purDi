# Basic Overview
**purDi** uses HuggingFace Diffusers' to generate images with Stable Diffusion. The GUI was designed with Qt Designer and PySide6. However, as this was a personal project to practice OOB Python, it will no longer be updated for the foreseeable future. In it's current state it should be useable up to Stable Diffusion v2.1.  

# Features
- text to image
- image to image - controlnet, cycle diffusion, depth-to-image, image variation, instructpix2pix, pix2pix zero-shot
- clothes segmentation (U2Net) by [levindabhi](https://github.com/levindabhi/cloth-segmentation) is used to create a black and white mask that is fed into Controlnet's image seg which then generates the same subject with different "fashionable" outfit. The opposite can be done as well, mask out the person and generate another person while maintain the original background.
- resizable left image browser that supports drag and drop into the center image viewer
- minimizable right side bar with double left mouse click
- prompt text field has a simple prompt "auto-complete" that suggests words that are defined through configs/prompts/words.txt

### Default view
![alt text](https://github.com/cvang187/purDi/blob/master/default_view.png?raw=true)  
### Customized view w/ hidden right side bar
![alt text](https://github.com/cvang187/purDi/blob/master/customized_view.png?raw=true)
