from mcp.server.fastmcp import FastMCP
from pptx import Presentation
from pptx.util import Pt

mcp = FastMCP("ppt_server")


@mcp.tool()
def create_presentation(filename: str) -> str:
    """Create a new PowerPoint presentation and save it to disk."""
    prs = Presentation()
    prs.save(filename)
    return f"Presentation '{filename}' created successfully."

@mcp.tool()
def plan_slides(topic: str, num_slides: int = 5) -> str:
    """Plan slide titles for a presentation topic before creating slides."""
    return f"Planning acknowledged for topic: '{topic}' with {num_slides} slides. Proceed to create_presentation next."

@mcp.tool()
def add_slide(filename: str, title: str, bullet_points: list[str]) -> str:
    """Load presentation from disk, add a slide, and save it back."""
    import os
    if not os.path.exists(filename):
        return f"Error: Presentation '{filename}' not found. Create it first."

    prs = Presentation(filename)
    slide_layout = prs.slide_layouts[1]  # Title + Content
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = title

    tf = slide.placeholders[1].text_frame
    tf.clear()
    for i, point in enumerate(bullet_points):
        if i == 0:
            tf.paragraphs[0].text = point
        else:
            p = tf.add_paragraph()
            p.text = point
        tf.paragraphs[i].level = 0

    prs.save(filename)
    return f"Slide '{title}' added to '{filename}'."


@mcp.tool()
def save_presentation(filename: str) -> str:
    """Confirm the presentation is saved on disk."""
    import os
    if not os.path.exists(filename):
        return f"Error: Presentation '{filename}' not found."
    return f"Presentation saved as '{filename}'."


if __name__ == "__main__":
    mcp.run()