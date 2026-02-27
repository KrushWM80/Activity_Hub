"""Initialize Design Library with example designs."""

import sys
from pathlib import Path

# Add parent to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.services.design_studio_service import DesignStudioService
from src.models.design_element import DesignElementType, DesignCategory


def initialize_example_designs():
    """Create example design elements for demonstration."""
    
    service = DesignStudioService()
    
    # Check if already initialized
    if service.get_statistics()["total_elements"] > 0:
        print("✅ Design library already contains elements. Skipping initialization.")
        return
    
    # Character example: Carl the Purple Monster
    carl = service.create_element(
        name="Carl - Purple Monster",
        element_type=DesignElementType.CHARACTER,
        description="A friendly, energetic purple monster character wearing Walmart blue vest. Carl is welcoming, motivational, and approachable. Uses expressive hand gestures.",
        prompt_template="Feature Carl, a friendly purple monster wearing a Walmart blue vest. He should be energetic, welcoming, and use expressive gestures. Carl is the primary character in this video.",
        created_by="system_init",
        category=DesignCategory.TRAINING,
        tags=["character", "friendly", "mascot", "training"],
        brand_colors=["#0071CE", "#FFB81C", "#7030A0"],
        personality_traits=["friendly", "energetic", "motivational", "approachable"],
        tone="friendly",
        usage_guidelines="Use Carl for training and motivational content. Perfect for onboarding and skill development videos.",
        restrictions="Carl should always wear Walmart blue vest. Keep expressions positive and welcoming."
    )
    if carl:
        service.approve_element(carl.id, "admin", "Example character - pre-approved")
        print(f"✅ Created and approved: {carl.name}")
    
    # Environment example: Walmart Store
    store = service.create_element(
        name="Walmart Store Environment",
        element_type=DesignElementType.ENVIRONMENT,
        description="Bright, professional Walmart store setting with checkout counters, aisles, and customers. Clean, well-lit environment with Walmart branding visible.",
        prompt_template="Set the scene in a modern Walmart store with bright lighting, clean aisles, and visible Walmart branding. Show a professional retail environment with customers and associates.",
        created_by="system_init",
        category=DesignCategory.OPERATIONS,
        tags=["environment", "store", "operations", "retail"],
        brand_colors=["#0071CE", "#FFB81C"],
        personality_traits=["professional", "clean", "modern"],
        tone="professional",
        usage_guidelines="Use for operations and customer service training content.",
        restrictions="Always keep Walmart branding visible and accurate."
    )
    if store:
        service.approve_element(store.id, "admin", "Example environment - pre-approved")
        print(f"✅ Created and approved: {store.name}")
    
    # Logo: Walmart Logo
    logo = service.create_element(
        name="Walmart Logo",
        element_type=DesignElementType.LOGO,
        description="Official Walmart logo with spark. Blue and yellow Walmart text with signature spark graphic.",
        prompt_template="Include the official Walmart logo (blue and yellow with spark) prominently displayed. Logo should be visible but not overwhelming.",
        created_by="system_init",
        category=DesignCategory.MARKETING,
        tags=["logo", "branding", "walmart"],
        brand_colors=["#0071CE", "#FFB81C"],
        personality_traits=["professional", "recognizable"],
        tone="professional",
        usage_guidelines="Always include Walmart logo in marketing and announcement content.",
        restrictions="Use only official Walmart logos. Must follow brand guidelines for sizing and placement."
    )
    if logo:
        service.approve_element(logo.id, "admin", "Example logo - pre-approved")
        print(f"✅ Created and approved: {logo.name}")
    
    # Animation Style: Energetic
    animation = service.create_element(
        name="Energetic Animation Style",
        element_type=DesignElementType.ANIMATION_STYLE,
        description="Fast-paced, dynamic animations with smooth transitions. Characters should move with energy and enthusiasm.",
        prompt_template="Use energetic, dynamic animations with smooth transitions. Movements should convey enthusiasm and forward momentum.",
        created_by="system_init",
        category=DesignCategory.TRAINING,
        tags=["animation", "energetic", "dynamic"],
        brand_colors=[],
        personality_traits=["energetic", "dynamic", "modern"],
        tone="friendly",
        usage_guidelines="Use for motivational training and recognition content.",
        restrictions="Maintain smooth transitions and avoid jarring movements."
    )
    if animation:
        service.approve_element(animation.id, "admin", "Example animation style - pre-approved")
        print(f"✅ Created and approved: {animation.name}")
    
    # Color scheme: Walmart Brand Colors
    colors = service.create_element(
        name="Walmart Brand Palette",
        element_type=DesignElementType.COLOR_SCHEME,
        description="Official Walmart color scheme: Walmart Blue (#0071CE), Walmart Yellow (#FFB81C), with supporting neutrals.",
        prompt_template="Use the official Walmart color palette: Walmart Blue (#0071CE) for primary elements, Walmart Yellow (#FFB81C) for accents, with white and neutral backgrounds.",
        created_by="system_init",
        category=DesignCategory.MARKETING,
        tags=["colors", "branding", "palette"],
        brand_colors=["#0071CE", "#FFB81C", "#FFFFFF", "#F0F0F0"],
        personality_traits=["professional", "recognizable", "trustworthy"],
        tone="professional",
        usage_guidelines="Always use for all professional content. Ensures brand consistency across facilities.",
        restrictions="Do not deviate from approved brand colors without prior approval."
    )
    if colors:
        service.approve_element(colors.id, "admin", "Example color scheme - pre-approved")
        print(f"✅ Created and approved: {colors.name}")
    
    # Final statistics
    stats = service.get_statistics()
    print("\n📊 Design Library Initialized:")
    print(f"   Total Elements: {stats['total_elements']}")
    print(f"   Approved: {stats['approved_elements']}")
    print(f"   By Type: {stats['by_type']}")


if __name__ == "__main__":
    initialize_example_designs()
