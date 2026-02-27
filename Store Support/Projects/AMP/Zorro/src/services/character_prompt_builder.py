"""Character prompt builder for creating consistent, granular character generation prompts."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class CharacterRole(str, Enum):
    """Character roles in Walmart context."""
    ASSOCIATE = "associate"
    MANAGER = "manager"
    CUSTOMER = "customer"
    SPECIALIST = "specialist"
    TRAINER = "trainer"


class SkinTone(str, Enum):
    """Skin tone options for diversity."""
    FAIR = "fair"
    LIGHT = "light"
    MEDIUM = "medium"
    OLIVE = "olive"
    TAN = "tan"
    DEEP = "deep"


class BodyType(str, Enum):
    """Body type options."""
    PETITE = "petite"
    AVERAGE = "average"
    ATHLETIC = "athletic"
    LARGER = "larger"


class AgeRange(str, Enum):
    """Age ranges."""
    YOUNG_ADULT = "18-25"
    ADULT = "25-40"
    MATURE = "40-55"
    SENIOR = "55+"


@dataclass
class CharacterAppearance:
    """Character physical appearance attributes."""
    age_range: AgeRange
    skin_tone: SkinTone
    body_type: BodyType
    hair_color: str  # e.g., "dark brown", "blonde", "red"
    hair_style: str  # e.g., "shoulder-length curly", "short neat", "long straight"
    eye_color: str  # e.g., "brown", "blue", "green"
    distinctive_features: List[str]  # e.g., ["glasses", "beard", "tattoo on arm"]
    clothing_style: str  # e.g., "professional blazer and slacks", "casual t-shirt and jeans"
    accessories: List[str]  # e.g., ["name badge", "watch", "earrings"]


@dataclass
class CharacterPersonality:
    """Character personality and behavior attributes."""
    primary_traits: List[str]  # e.g., ["friendly", "professional", "energetic", "patient"]
    communication_style: str  # e.g., "warm and approachable", "direct and efficient"
    mannerisms: List[str]  # e.g., ["smiles frequently", "makes eye contact", "gestures when speaking"]
    speaking_pace: str  # e.g., "conversational", "measured", "quick"
    expressions: List[str]  # e.g., ["warm smile", "attentive expression", "focused frown"]
    emotional_tone: str  # e.g., "positive and upbeat", "calm and composed"


@dataclass
class CharacterContext:
    """Character context and role attributes."""
    role: CharacterRole
    department: Optional[str]  # e.g., "Customer Service", "Grocery", "Electronics"
    typical_environments: List[str]  # e.g., ["store floor", "break room", "cash register"]
    expertise_areas: List[str]  # e.g., ["product knowledge", "customer service", "team leadership"]
    common_activities: List[str]  # e.g., ["helping customers find items", "stocking shelves", "training"]


@dataclass
class CharacterBrand:
    """Brand-specific attributes."""
    brand_colors: List[str]  # e.g., ["#0071CE", "#FFB81C"]
    uniform_description: str  # e.g., "Walmart vest over casual shirt"
    brand_personality_alignment: str  # How character aligns with brand values


class CharacterPromptBuilder:
    """
    Builds detailed, granular character generation prompts that create
    consistent characters across multiple videos and contexts.
    """
    
    def __init__(self):
        """Initialize the character prompt builder."""
        self.template = self._build_template()
    
    def build_prompt(
        self,
        character_name: str,
        appearance: CharacterAppearance,
        personality: CharacterPersonality,
        context: CharacterContext,
        brand: CharacterBrand,
        additional_notes: Optional[str] = None
    ) -> str:
        """
        Build a comprehensive character generation prompt.
        
        Args:
            character_name: Character name
            appearance: Physical appearance details
            personality: Personality and behavior details
            context: Role and context details
            brand: Brand-specific details
            additional_notes: Any additional guidance
        
        Returns:
            str: Detailed prompt for AI character generation
        """
        prompt_sections = []
        
        # Character identity
        prompt_sections.append(self._build_identity_section(character_name, context))
        
        # Physical appearance
        prompt_sections.append(self._build_appearance_section(appearance))
        
        # Personality and behavior
        prompt_sections.append(self._build_personality_section(personality))
        
        # Role and context
        prompt_sections.append(self._build_context_section(context))
        
        # Brand alignment
        prompt_sections.append(self._build_brand_section(brand))
        
        # Generation guidelines
        prompt_sections.append(self._build_guidelines_section())
        
        # Additional notes
        if additional_notes:
            prompt_sections.append(f"Additional Guidance:\n{additional_notes}")
        
        # Combine all sections
        full_prompt = "\n\n".join(prompt_sections)
        
        return full_prompt
    
    def _build_identity_section(self, name: str, context: CharacterContext) -> str:
        """Build character identity section."""
        return f"""CHARACTER IDENTITY
================

Name: {name}
Role: {context.role.value}
Department: {context.department or 'General'}

This character embodies consistency, appearing the same way across different messages, weeks, and contexts.
Their appearance, mannerisms, and presence should be instantly recognizable."""
    
    def _build_appearance_section(self, appearance: CharacterAppearance) -> str:
        """Build physical appearance section."""
        distinctive = ", ".join(appearance.distinctive_features) if appearance.distinctive_features else "none"
        accessories = ", ".join(appearance.accessories) if appearance.accessories else "none"
        
        return f"""PHYSICAL APPEARANCE
===================

CRITICAL: CARTOON/PIXAR STYLE - NOT PHOTOREALISTIC
- This character MUST be rendered in cartoon animation style
- Similar to Pixar character design (like characters from Toy Story, Monsters Inc)
- Exaggerated, stylized features (not realistic human faces)
- Use bright, appealing colors and proportions
- Animated style with clear outlines and shading

Age Range: {appearance.age_range.value}
Skin Tone: {appearance.skin_tone.value}
Body Type: {appearance.body_type.value}

Hair:
- Color: {appearance.hair_color}
- Style: {appearance.hair_style}

Eyes: {appearance.eye_color} (stylized, expressive)

Distinctive Features: {distinctive}

Clothing:
- Style: {appearance.clothing_style}
- Accessories: {accessories}

ANIMATION STYLE REQUIREMENTS:
- Cartoon animation only (Pixar/DreamWorks style)
- Exaggerated proportions and expressions
- NO photorealistic or live-action rendering
- Clear, bold lines and vibrant colors
- Friendly, approachable design
- Professional yet approachable appearance
- Same cartoon style in every video"""
    
    def _build_personality_section(self, personality: CharacterPersonality) -> str:
        """Build personality and behavior section."""
        traits = ", ".join(personality.primary_traits)
        ", ".join(personality.mannerisms)
        ", ".join(personality.expressions)
        
        return f"""PERSONALITY & BEHAVIOR
======================

Core Traits: {traits}
Communication Style: {personality.communication_style}
Speaking Pace: {personality.speaking_pace}
Emotional Tone: {personality.emotional_tone}

Mannerisms:
- {chr(10).join("- " + m for m in personality.mannerisms)}

Typical Expressions:
- {chr(10).join("- " + e for e in personality.expressions)}

Behavioral Consistency:
- This character should display consistent personality across all videos
- Use the same mannerisms, expressions, and communication style
- Maintain emotional tone in different contexts
- Personality traits should be evident in body language and facial expressions"""
    
    def _build_context_section(self, context: CharacterContext) -> str:
        """Build role and context section."""
        ", ".join(context.typical_environments)
        ", ".join(context.expertise_areas)
        ", ".join(context.common_activities)
        
        return f"""ROLE & CONTEXT
===============

Role: {context.role.value}
Department: {context.department or 'N/A'}

Typical Environments:
- {chr(10).join("- " + env for env in context.typical_environments)}

Areas of Expertise:
- {chr(10).join("- " + exp for exp in context.expertise_areas)}

Common Activities:
- {chr(10).join("- " + act for act in context.common_activities)}

Context Usage:
- Generate this character in appropriate environments for their role
- Show them engaged in activities relevant to their expertise
- Maintain professional demeanor appropriate to their department"""
    
    def _build_brand_section(self, brand: CharacterBrand) -> str:
        """Build brand alignment section."""
        colors = ", ".join(brand.brand_colors)
        
        return f"""BRAND ALIGNMENT
================

Walmart Brand Colors: {colors}
Uniform Description: {brand.uniform_description}
Brand Alignment: {brand.brand_personality_alignment}

Brand Integration:
- Character should wear Walmart uniform consistently
- Use brand colors appropriately in environment
- Character should embody Walmart values of customer service excellence
- Professional appearance aligned with corporate standards"""
    
    def _build_guidelines_section(self) -> str:
        """Build generation guidelines section."""
        return """GENERATION GUIDELINES
=====================

1. ANIMATION STYLE - MANDATORY
   - ONLY cartoon animation (Pixar/DreamWorks style)
   - Exaggerated features and proportions
   - NO photorealistic faces or human-like rendering
   - NO live-action or realistic human appearances
   - Bright, vibrant colors
   - Clear outlines and bold strokes
   - Professional animation quality

2. CHARACTER CONSISTENCY
   - Generate the exact same cartoon character in every video
   - Same appearance, mannerisms, and personality
   - Facial features should be instantly recognizable
   - Use these descriptions as immutable constraints

3. REUSABILITY ACROSS CONTEXTS
   - This prompt should work for any message/scenario
   - Character appearance remains consistent even in different contexts
   - Personality should shine through regardless of activity

4. VIDEO QUALITY
   - Clear, well-lit animated scenes showing character clearly
   - Professional animation composition
   - Expressions and mannerisms clearly visible
   - Character in typical work environment when appropriate

5. DURATION
   - Videos should be 8 seconds
   - Allow enough time to show character personality
   - Include character movements and expressions

6. DO NOT DEVIATE
   - Every video must show this cartoon character the same way
   - Do not create variations or interpretations
   - Use exact descriptors provided above
   - Consistency is more important than creativity
   - Maintain cartoon/Pixar style in all outputs"""
    
    def _build_template(self) -> str:
        """Return template structure."""
        return """
[CHARACTER IDENTITY]
[APPEARANCE]
[PERSONALITY]
[CONTEXT]
[BRAND]
[GUIDELINES]
"""
    
    def build_quick_prompt(self, character_name: str, base_description: str) -> str:
        """
        Build a simpler prompt from just name and description.
        
        Useful for quick character creation without full attribute collection.
        
        Args:
            character_name: Character name
            base_description: Brief character description
        
        Returns:
            str: Usable character generation prompt
        """
        return f"""Generate a CARTOON/PIXAR-STYLE character named {character_name} with the following characteristics:

{base_description}

CRITICAL REQUIREMENTS:
- ANIMATION STYLE: Cartoon animation only (like Pixar/DreamWorks)
- NO photorealistic or human-like faces
- Exaggerated, stylized features and proportions
- This character must appear EXACTLY the same in every video
- Every time you generate a video with this prompt, produce the identical cartoon character
- Same appearance, clothing, mannerisms, and personality
- Character should be instantly recognizable across videos
- Focus on consistency over variation
- Bright, vibrant colors and professional animation quality

Generate the character in a professional Walmart store environment.
Duration: 8 seconds
Show clear facial expressions and natural mannerisms."""
    
    def enhance_existing_prompt(self, base_prompt: str) -> str:
        """
        Enhance an existing character prompt with consistency requirements.
        
        Args:
            base_prompt: Existing character prompt
        
        Returns:
            str: Enhanced prompt with consistency focus
        """
        consistency_addon = """

--- CONSISTENCY & STYLE ENHANCEMENT ---

ANIMATION STYLE (MANDATORY):
- Render as CARTOON/PIXAR animation style ONLY
- NO photorealistic or realistic human faces
- Exaggerated, stylized features (Toy Story, Monsters Inc style)
- Bright, vibrant colors
- Clear outlines and professional animation

For MAXIMUM CHARACTER CONSISTENCY across all videos:

1. VISUAL ANCHORS (Use these to ensure recognition):
   - Specific cartoon features that must remain identical
   - Exact clothing items and colors
   - Distinctive mannerisms or expressions
   - Specific accessories or badges
   - Cartoon animation style maintained

2. CONTEXT-AGNOSTIC DESIGN:
   - This character should work in any Walmart context
   - Appearance should remain constant regardless of scenario
   - Personality should shine through in all situations

3. REUSABILITY:
   - This prompt will be used repeatedly across different messages and weeks
   - Generate the same cartoon character every single time
   - Consistency is the primary goal

4. IMPLEMENTATION:
   - Every video generation must produce recognizable cartoon character
   - Use provided descriptions as immutable constraints
   - Do not create variations or alternative versions
   - Maintain cartoon/Pixar animation style consistently
   - Familiarity builds over time with repeated appearances"""
        
        return base_prompt + consistency_addon
