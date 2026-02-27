"""Service for managing design elements and templates."""

import json
import logging
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.models.design_element import (
    DesignCategory,
    DesignElement,
    DesignElementType,
    DesignLibrary,
    ProductionTemplate,
)

logger = logging.getLogger(__name__)


# Input validation constants
MAX_NAME_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 5000
MAX_PROMPT_LENGTH = 10000
MAX_TAG_LENGTH = 50
MAX_TAGS_COUNT = 20
VALID_NAME_PATTERN = re.compile(r'^[\w\s\-\.\,\!\?\(\)]+$', re.UNICODE)


class InputValidationError(ValueError):
    """Raised when input validation fails."""
    pass


def _sanitize_string(value: str, field_name: str, max_length: int) -> str:
    """Sanitize and validate string input."""
    if not isinstance(value, str):
        raise InputValidationError(f"{field_name} must be a string")
    
    # Strip whitespace
    value = value.strip()
    
    # Check length
    if len(value) > max_length:
        raise InputValidationError(
            f"{field_name} exceeds maximum length of {max_length} characters"
        )
    
    # Check for empty after strip
    if not value:
        raise InputValidationError(f"{field_name} cannot be empty")
    
    return value


def _validate_name(name: str) -> str:
    """Validate element name."""
    name = _sanitize_string(name, "name", MAX_NAME_LENGTH)
    
    if not VALID_NAME_PATTERN.match(name):
        raise InputValidationError(
            "Name contains invalid characters. Use only letters, numbers, spaces, "
            "and basic punctuation (- . , ! ? ( ))"
        )
    
    return name


def _validate_tags(tags: Optional[List[str]]) -> List[str]:
    """Validate and sanitize tags."""
    if tags is None:
        return []
    
    if not isinstance(tags, list):
        raise InputValidationError("Tags must be a list")
    
    if len(tags) > MAX_TAGS_COUNT:
        raise InputValidationError(f"Maximum {MAX_TAGS_COUNT} tags allowed")
    
    validated = []
    for tag in tags:
        if not isinstance(tag, str):
            continue
        tag = tag.strip().lower()
        if tag and len(tag) <= MAX_TAG_LENGTH:
            # Only alphanumeric and hyphens
            if re.match(r'^[\w\-]+$', tag):
                validated.append(tag)
    
    return list(set(validated))  # Remove duplicates


class DesignStudioService:
    """Manages design elements for consistent content creation."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize Design Studio Service.
        
        Args:
            storage_path: Path to store design library JSON
        """
        self.storage_path = storage_path or Path("data/design_library.json")
        self.templates_path = self.storage_path.parent / "production_templates.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.library = self._load_library()
        self.templates: List[ProductionTemplate] = self._load_templates()
    
    def _load_library(self) -> DesignLibrary:
        """Load design library from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    return DesignLibrary(**data)
            except Exception as e:
                logger.error(f"Failed to load design library: {e}")
                return DesignLibrary()
        return DesignLibrary()
    
    def _save_library(self) -> bool:
        """Save design library to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.library.model_dump(mode='json'), f, indent=2, default=str)
            logger.info(f"Design library saved to {self.storage_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save design library: {e}")
            return False
    
    def _load_templates(self) -> List[ProductionTemplate]:
        """Load production templates from storage."""
        if self.templates_path.exists():
            try:
                with open(self.templates_path, 'r') as f:
                    data = json.load(f)
                    return [ProductionTemplate(**t) for t in data.get("templates", [])]
            except Exception as e:
                logger.error(f"Failed to load production templates: {e}")
                return []
        return []
    
    def _save_templates(self) -> bool:
        """Save production templates to storage."""
        try:
            data = {
                "templates": [t.model_dump(mode='json') for t in self.templates],
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            with open(self.templates_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Production templates saved to {self.templates_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save production templates: {e}")
            return False
    
    # =========================================================================
    # Production Template Management
    # =========================================================================
    
    def create_production_template(
        self,
        name: str,
        created_by: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        character_id: Optional[str] = None,
        environment_id: Optional[str] = None,
        logo_id: Optional[str] = None,
        color_scheme_id: Optional[str] = None,
        default_duration: int = 6,
        default_aspect_ratio: str = "16:9",
        prompt_prefix: Optional[str] = None,
        prompt_suffix: Optional[str] = None,
        negative_prompt: Optional[str] = None
    ) -> Optional[ProductionTemplate]:
        """
        Create a new production template.
        
        Args:
            name: Template display name
            created_by: User ID
            description: Template description
            category: Target message category
            character_id: Character element ID
            environment_id: Environment element ID
            logo_id: Logo element ID
            color_scheme_id: Color scheme ID
            default_duration: Default video duration
            default_aspect_ratio: Default aspect ratio
            prompt_prefix: Text to prepend to prompts
            prompt_suffix: Text to append to prompts
            negative_prompt: What to avoid
            
        Returns:
            Created ProductionTemplate or None if failed
        """
        try:
            name = _validate_name(name)
            created_by = _sanitize_string(created_by, "created_by", MAX_NAME_LENGTH)
            
            template_id = f"template_{uuid.uuid4().hex[:8]}"
            
            template = ProductionTemplate(
                id=template_id,
                name=name,
                description=description,
                category=category,
                character_id=character_id,
                environment_id=environment_id,
                logo_id=logo_id,
                color_scheme_id=color_scheme_id,
                default_duration=default_duration,
                default_aspect_ratio=default_aspect_ratio,
                prompt_prefix=prompt_prefix,
                prompt_suffix=prompt_suffix,
                negative_prompt=negative_prompt,
                created_by=created_by
            )
            
            self.templates.append(template)
            self._save_templates()
            
            logger.info(f"Created production template: {template_id}")
            return template
            
        except Exception as e:
            logger.error(f"Failed to create production template: {e}")
            return None
    
    def get_template(self, template_id: str) -> Optional[ProductionTemplate]:
        """Get a production template by ID."""
        for template in self.templates:
            if template.id == template_id:
                return template
        return None
    
    def list_templates(
        self,
        category: Optional[str] = None,
        active_only: bool = True
    ) -> List[ProductionTemplate]:
        """
        List production templates.
        
        Args:
            category: Filter by target category
            active_only: Only return active templates
            
        Returns:
            List of matching templates
        """
        results = self.templates
        
        if active_only:
            results = [t for t in results if t.is_active]
        
        if category:
            results = [t for t in results if t.category == category]
        
        return sorted(results, key=lambda t: t.usage_count, reverse=True)
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a production template."""
        for i, template in enumerate(self.templates):
            if template.id == template_id:
                self.templates.pop(i)
                self._save_templates()
                logger.info(f"Deleted production template: {template_id}")
                return True
        return False
    
    def get_template_elements(self, template: ProductionTemplate) -> Dict[str, Optional[DesignElement]]:
        """
        Get all design elements for a production template.
        
        Args:
            template: The production template
            
        Returns:
            Dict mapping element type to DesignElement (or None if not found)
        """
        return {
            "character": self.get_element(template.character_id) if template.character_id else None,
            "environment": self.get_element(template.environment_id) if template.environment_id else None,
            "logo": self.get_element(template.logo_id) if template.logo_id else None,
            "color_scheme": self.get_element(template.color_scheme_id) if template.color_scheme_id else None,
        }
    
    def build_template_prompt(
        self,
        template: ProductionTemplate,
        message_content: str
    ) -> str:
        """
        Build a complete prompt using a production template.
        
        Args:
            template: The production template
            message_content: The AMP message content
            
        Returns:
            Complete prompt with all element prompts combined
        """
        parts = []
        
        # Add prefix if present
        if template.prompt_prefix:
            parts.append(template.prompt_prefix)
        
        # Add design element prompts
        elements = self.get_template_elements(template)
        
        if elements.get("character"):
            parts.append(elements["character"].prompt_template)
        
        if elements.get("environment"):
            parts.append(elements["environment"].prompt_template)
        
        if elements.get("logo"):
            parts.append(elements["logo"].prompt_template)
        
        # Add the message content
        parts.append(message_content)
        
        # Add suffix if present
        if template.prompt_suffix:
            parts.append(template.prompt_suffix)
        
        # Increment usage
        template.increment_usage()
        self._save_templates()
        
        return " ".join(parts)
    
    def create_element(
        self,
        name: str,
        element_type: DesignElementType,
        description: str,
        prompt_template: str,
        created_by: str,
        category: DesignCategory = DesignCategory.CUSTOM,
        tags: Optional[List[str]] = None,
        visual_reference_path: Optional[str] = None,
        facility_id: str = "global",
        **metadata_kwargs
    ) -> Optional[DesignElement]:
        """
        Create a new design element.
        
        Args:
            name: Display name
            element_type: Type of element
            description: Visual description
            prompt_template: LLM injection template
            created_by: User ID
            category: Content category
            tags: Searchable tags
            visual_reference_path: Path to reference image/video
            facility_id: Creating facility
            **metadata_kwargs: Additional metadata fields
            
        Returns:
            Created DesignElement or None if failed
            
        Raises:
            InputValidationError: If input validation fails
        """
        try:
            # Validate inputs
            name = _validate_name(name)
            description = _sanitize_string(description, "description", MAX_DESCRIPTION_LENGTH)
            prompt_template = _sanitize_string(prompt_template, "prompt_template", MAX_PROMPT_LENGTH)
            created_by = _sanitize_string(created_by, "created_by", MAX_NAME_LENGTH)
            tags = _validate_tags(tags)
            
            # Validate facility_id
            if facility_id:
                facility_id = _sanitize_string(facility_id, "facility_id", 100)
            
            element_id = f"{element_type.value}_{uuid.uuid4().hex[:8]}"
            
            from src.models.design_element import DesignMetadata

            # Filter metadata to only valid fields and ensure they're not DesignMetadata instances
            valid_metadata = {}
            for k, v in metadata_kwargs.items():
                if k in DesignMetadata.model_fields:
                    # Don't pass DesignMetadata instances - let the constructor create it
                    if not isinstance(v, DesignMetadata):
                        valid_metadata[k] = v
            
            metadata = DesignMetadata(**valid_metadata)
            
            element = DesignElement(
                id=element_id,
                name=name,
                type=element_type,
                description=description,
                prompt_template=prompt_template,
                created_by=created_by,
                category=category,
                tags=tags or [],
                visual_reference_path=visual_reference_path,
                facility_id=facility_id,
                metadata=metadata.model_dump(),  # Pass as dict for proper serialization
            )
            
            # Add to appropriate collection
            self._add_to_library(element)
            self._save_library()
            
            logger.info(f"Created design element: {element_id}")
            return element
            
        except Exception as e:
            logger.error(f"Failed to create design element: {e}", exc_info=True)
            raise  # Re-raise so caller can see the error
    
    def _add_to_library(self, element: DesignElement) -> None:
        """Add element to library in correct collection."""
        if element.type == DesignElementType.CHARACTER:
            self.library.characters.append(element)
        elif element.type == DesignElementType.LOGO:
            self.library.logos.append(element)
        elif element.type == DesignElementType.ENVIRONMENT:
            self.library.environments.append(element)
        elif element.type == DesignElementType.PROP:
            self.library.props.append(element)
        elif element.type == DesignElementType.ANIMATION_STYLE:
            self.library.animation_styles.append(element)
        elif element.type == DesignElementType.COLOR_SCHEME:
            self.library.color_schemes.append(element)
    
    def get_element(self, element_id: str) -> Optional[DesignElement]:
        """Retrieve a specific design element by ID."""
        for collection in [
            self.library.characters, self.library.logos,
            self.library.environments, self.library.props,
            self.library.animation_styles, self.library.color_schemes
        ]:
            for element in collection:
                if element.id == element_id:
                    return element
        return None
    
    def get_elements_by_type(self, element_type: DesignElementType) -> List[DesignElement]:
        """
        Get all elements of a specific type.
        
        Convenience method that wraps list_elements.
        
        Args:
            element_type: Type of elements to retrieve
            
        Returns:
            List of design elements of the specified type
        """
        return self.list_elements(element_type=element_type)
    
    def list_elements(
        self,
        element_type: Optional[DesignElementType] = None,
        category: Optional[DesignCategory] = None,
        tags: Optional[List[str]] = None,
        facility_id: Optional[str] = None,
        approved_only: bool = False
    ) -> List[DesignElement]:
        """
        List design elements with optional filtering.
        
        Args:
            element_type: Filter by type
            category: Filter by category
            tags: Filter by tags (any match)
            facility_id: Filter by facility
            approved_only: Only approved elements
            
        Returns:
            Filtered list of design elements
        """
        results = []
        
        for collection in [
            self.library.characters, self.library.logos,
            self.library.environments, self.library.props,
            self.library.animation_styles, self.library.color_schemes
        ]:
            for element in collection:
                # Type filter
                if element_type and element.type != element_type:
                    continue
                
                # Category filter
                if category and element.category != category:
                    continue
                
                # Facility filter
                if facility_id and element.facility_id != facility_id:
                    continue
                
                # Approval filter
                if approved_only and not element.is_approved:
                    continue
                
                # Tag filter (any match)
                if tags:
                    if not any(tag in element.tags for tag in tags):
                        continue
                
                results.append(element)
        
        return results
    
    def update_element(
        self,
        element_id: str,
        **updates
    ) -> Optional[DesignElement]:
        """
        Update a design element.
        
        Args:
            element_id: Element to update
            **updates: Fields to update
            
        Returns:
            Updated DesignElement or None
        """
        element = self.get_element(element_id)
        if not element:
            return None
        
        try:
            # Update allowed fields
            for key, value in updates.items():
                if key in element.model_fields and key not in ['id', 'created_at']:
                    setattr(element, key, value)
            
            element.updated_at = datetime.now(timezone.utc)
            self._save_library()
            
            logger.info(f"Updated design element: {element_id}")
            return element
            
        except Exception as e:
            logger.error(f"Failed to update design element: {e}")
            return None
    
    def delete_element(self, element_id: str) -> bool:
        """
        Delete a design element.
        
        Args:
            element_id: Element to delete
            
        Returns:
            True if deleted, False otherwise
        """
        for collection in [
            self.library.characters, self.library.logos,
            self.library.environments, self.library.props,
            self.library.animation_styles, self.library.color_schemes
        ]:
            for i, element in enumerate(collection):
                if element.id == element_id:
                    collection.pop(i)
                    self._save_library()
                    logger.info(f"Deleted design element: {element_id}")
                    return True
        
        return False
    
    def approve_element(
        self,
        element_id: str,
        approved_by: str,
        approval_notes: str = ""
    ) -> Optional[DesignElement]:
        """
        Approve a design element for use.
        
        Args:
            element_id: Element to approve
            approved_by: Admin ID
            approval_notes: Comments
            
        Returns:
            Updated DesignElement
        """
        element = self.get_element(element_id)
        if not element:
            return None
        
        element.is_approved = True
        element.approved_by = approved_by
        element.approval_notes = approval_notes
        element.updated_at = datetime.now(timezone.utc)
        
        self._save_library()
        logger.info(f"Approved design element: {element_id}")
        
        return element
    
    def reject_element(
        self,
        element_id: str,
        rejected_by: str,
        rejection_reason: str
    ) -> Optional[DesignElement]:
        """
        Reject a design element with feedback.
        
        Args:
            element_id: Element to reject
            rejected_by: Admin ID
            rejection_reason: Why rejected
            
        Returns:
            Updated DesignElement
        """
        element = self.get_element(element_id)
        if not element:
            return None
        
        element.is_approved = False
        element.approved_by = rejected_by
        element.approval_notes = f"REJECTED: {rejection_reason}"
        element.updated_at = datetime.now(timezone.utc)
        
        self._save_library()
        logger.info(f"Rejected design element: {element_id}")
        
        return element
    
    def search(
        self,
        query: str,
        element_type: Optional[DesignElementType] = None
    ) -> List[DesignElement]:
        """
        Search design elements by name, description, or tags.
        
        Args:
            query: Search query
            element_type: Optional type filter
            
        Returns:
            Matching design elements
        """
        query_lower = query.lower()
        results = []
        
        for collection in [
            self.library.characters, self.library.logos,
            self.library.environments, self.library.props,
            self.library.animation_styles, self.library.color_schemes
        ]:
            for element in collection:
                if element_type and element.type != element_type:
                    continue
                
                # Search in name, description, tags
                if (query_lower in element.name.lower() or
                    query_lower in element.description.lower() or
                    any(query_lower in tag for tag in element.tags)):
                    results.append(element)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get library statistics."""
        all_elements = (
            self.library.characters + self.library.logos +
            self.library.environments + self.library.props +
            self.library.animation_styles + self.library.color_schemes
        )
        
        approved = [e for e in all_elements if e.is_approved]
        total_usage = sum(e.usage_count for e in all_elements)
        
        return {
            "total_elements": len(all_elements),
            "approved_elements": len(approved),
            "pending_approval": len(all_elements) - len(approved),
            "total_usage": total_usage,
            "by_type": {
                "characters": len(self.library.characters),
                "logos": len(self.library.logos),
                "environments": len(self.library.environments),
                "props": len(self.library.props),
                "animation_styles": len(self.library.animation_styles),
                "color_schemes": len(self.library.color_schemes),
            },
            "most_used": sorted(all_elements, key=lambda x: x.usage_count, reverse=True)[:10],
        }
    
    def increment_usage(self, element_id: str) -> bool:
        """Increment usage counter for an element."""
        element = self.get_element(element_id)
        if element:
            element.increment_usage()
            self._save_library()
            return True
        return False
    
    def export_library(self) -> Dict[str, Any]:
        """Export entire library as JSON-compatible dict."""
        return self.library.model_dump(mode='json')
    
    def export_by_facility(self, facility_id: str) -> Dict[str, Any]:
        """Export design elements accessible to a specific facility."""
        accessible = self.list_elements(
            facility_id=facility_id,
            approved_only=True
        )
        
        library_copy = DesignLibrary()
        for element in accessible:
            self._add_to_library_copy(library_copy, element)
        
        return library_copy.model_dump(mode='json')
    
    def _add_to_library_copy(self, lib: DesignLibrary, elem: DesignElement) -> None:
        """Helper to add element to a library copy."""
        if elem.type == DesignElementType.CHARACTER:
            lib.characters.append(elem)
        elif elem.type == DesignElementType.LOGO:
            lib.logos.append(elem)
        elif elem.type == DesignElementType.ENVIRONMENT:
            lib.environments.append(elem)
        elif elem.type == DesignElementType.PROP:
            lib.props.append(elem)
        elif elem.type == DesignElementType.ANIMATION_STYLE:
            lib.animation_styles.append(elem)
        elif elem.type == DesignElementType.COLOR_SCHEME:
            lib.color_schemes.append(elem)
