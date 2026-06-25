
import re

def prepare_for_llm(markdown_text: str) -> str:
    """
    Hides base64 images to save tokens and prevent text splitters 
    from breaking the image-unit blocks.
    """
    return re.sub(
        r'(<img\s+[^>]*src=")data:image/[^"]+(")',
        r'\1[IMAGE_HIDDEN]\2',
        markdown_text,
        flags=re.IGNORECASE
    )

def extract_descriptions_only(markdown_text: str) -> str:
    """
    Strips out the images entirely and keeps ONLY the description text.
    Useful if you want to feed pure text to an LLM without even the HTML tags.
    """
    def replacer(match):
        # Return just the inner content of the description tag
        return match.group(1).strip()
    
    return re.sub(
        r'<image-unit>.*?<image-description>\s*(.*?)\s*</image-description>.*?</image-unit>',
        replacer,
        markdown_text,
        flags=re.IGNORECASE | re.DOTALL
    )

def restore_base64_images(markdown_text: str, original_base64_map: dict) -> str:
    """
    If you hid images for the LLM, you can restore them for the UI.
    (Assuming you saved the original base64 strings somewhere).
    """
    # Implementation depends on how you store the original base64 map
    # Example logic:
    # for placeholder, real_base64 in original_base64_map.items():
    #     markdown_text = markdown_text.replace(placeholder, real_base64)
    return markdown_text
