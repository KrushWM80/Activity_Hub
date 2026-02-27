"""Quick Demo of Design Studio Features."""

import sys
from pathlib import Path

# Add parent to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.services.design_studio_service import DesignStudioService
from src.models.design_element import DesignElementType, DesignCategory


def demo_design_studio():
    """Demonstrate Design Studio capabilities."""
    
    print("🎨 Design Studio Demo")
    print("=" * 60)
    
    service = DesignStudioService()
    
    # Get existing designs
    print("\n📚 Design Library Contents:")
    print("-" * 60)
    
    stats = service.get_statistics()
    print(f"Total Elements: {stats['total_elements']}")
    print(f"Approved: {stats['approved_elements']}")
    print(f"\nBy Type:")
    for elem_type, count in stats['by_type'].items():
        print(f"  - {elem_type}: {count}")
    
    # Show all designs
    print("\n" + "=" * 60)
    print("📋 Available Designs:")
    print("=" * 60)
    
    all_elements = service.list_elements()
    for elem in all_elements:
        print(f"\n✅ {elem.name}")
        print(f"   Type: {elem.type.value}")
        print(f"   Category: {elem.category.value}")
        print(f"   Status: {'APPROVED' if elem.is_approved else 'PENDING'}")
        print(f"   Usage Count: {elem.usage_count}")
        print(f"   Description: {elem.description}")
        print(f"   Tags: {', '.join(elem.tags)}")
    
    # Demo search
    print("\n" + "=" * 60)
    print("🔍 Search Demo - Finding 'Carl':")
    print("=" * 60)
    
    results = service.search("carl")
    for elem in results:
        print(f"✅ Found: {elem.name}")
        print(f"   ID: {elem.id}")
        print(f"   Type: {elem.type.value}")
    
    # Demo filtering by type
    print("\n" + "=" * 60)
    print("🎬 Filter Demo - Characters Only:")
    print("=" * 60)
    
    characters = service.list_elements(element_type=DesignElementType.CHARACTER)
    for char in characters:
        print(f"✅ {char.name}")
        print(f"   Personality: {char.metadata.personality or 'N/A'}")
        print(f"   Use Cases: {', '.join(char.metadata.use_cases) if char.metadata.use_cases else 'N/A'}")
    
    # Demo prompt injection
    print("\n" + "=" * 60)
    print("🎯 Prompt Injection Demo:")
    print("=" * 60)
    
    selected_elements = {
        "character": service.search("carl")[0] if service.search("carl") else None,
        "environment": service.list_elements(element_type=DesignElementType.ENVIRONMENT)[0] 
                      if service.list_elements(element_type=DesignElementType.ENVIRONMENT) else None,
        "color_scheme": service.list_elements(element_type=DesignElementType.COLOR_SCHEME)[0]
                       if service.list_elements(element_type=DesignElementType.COLOR_SCHEME) else None,
    }
    
    print("Selected Elements:")
    for type_key, elem in selected_elements.items():
        if elem:
            print(f"  - {type_key}: {elem.name}")
    
    print("\nComposite Prompt (for injection into message):")
    print("-" * 60)
    
    composite_parts = []
    for elem in selected_elements.values():
        if elem:
            composite_parts.append(elem.prompt_template)
            print(f"\n[{elem.name}]")
            print(elem.prompt_template)
    
    print("\n" + "-" * 60)
    print("Final Composite Prompt:")
    print("-" * 60)
    composite = " ".join(composite_parts)
    print(composite)
    
    # Demo usage tracking
    print("\n" + "=" * 60)
    print("📊 Usage Tracking Demo:")
    print("=" * 60)
    
    if selected_elements["character"]:
        elem_id = selected_elements["character"].id
        print(f"Incrementing usage for: {selected_elements['character'].name}")
        
        # Get current usage
        elem = service.get_element(elem_id)
        print(f"Usage before: {elem.usage_count}")
        
        # Increment
        service.increment_usage(elem_id)
        
        # Get updated usage
        elem = service.get_element(elem_id)
        print(f"Usage after: {elem.usage_count}")
    
    # Demo most used elements
    print("\n" + "=" * 60)
    print("🏆 Most Used Elements:")
    print("=" * 60)
    
    stats = service.get_statistics()
    for elem in stats['most_used'][:5]:
        print(f"  {elem.name}: {elem.usage_count} uses")
    
    # Demo API example
    print("\n" + "=" * 60)
    print("💻 API Usage Example:")
    print("=" * 60)
    
    print("""
# Create a new design element
element = service.create_element(
    name="Tony the Tiger",
    element_type=DesignElementType.CHARACTER,
    description="Energetic tiger mascot for safety campaigns",
    prompt_template="Feature Tony the Tiger, energetic and motivational...",
    created_by="manager_123",
    category=DesignCategory.SAFETY,
    tags=["safety", "mascot", "tiger"]
)

# Approve it (admin only)
service.approve_element(element.id, "admin_user", "Approved")

# Get it by ID
elem = service.get_element(element.id)

# Search for it
results = service.search("tony")

# List with filters
safety_chars = service.list_elements(
    element_type=DesignElementType.CHARACTER,
    category=DesignCategory.SAFETY,
    approved_only=True
)

# Track usage
service.increment_usage(element.id)

# Get statistics
stats = service.get_statistics()
print(f"Total elements: {stats['total_elements']}")
print(f"Total usage: {stats['total_usage']}")
    """)
    
    print("\n✅ Design Studio Demo Complete!\n")


if __name__ == "__main__":
    demo_design_studio()
