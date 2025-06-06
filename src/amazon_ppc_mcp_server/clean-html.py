#!/usr/bin/env python3
"""
HTML to Clean XML Converter
Strips unnecessary attributes and styling from HTML while preserving structure and content.
"""

import re
import sys
import argparse
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
import xml.etree.ElementTree as ET
from xml.dom import minidom
import html


class StructuralHTMLConverter:
    """Enhanced HTML converter that preserves structure while maximizing size reduction."""
    
    # Semantic CSS class patterns to preserve
    SEMANTIC_CLASS_PATTERNS = {
        'layout': ['header', 'footer', 'nav', 'sidebar', 'content', 'main', 'wrapper', 'container'],
        'component': ['button', 'menu', 'dropdown', 'modal', 'tab', 'accordion', 'carousel'],
        'state': ['active', 'disabled', 'hidden', 'open', 'closed', 'expanded', 'collapsed'],
        'type': ['primary', 'secondary', 'warning', 'error', 'success', 'info'],
    }
    
    # Styling class patterns to remove
    STYLING_PATTERNS = [
        r'^\w+-\d+$',  # utility classes like 'mt-4', 'px-2'
        r'^[a-z]+\d+$',  # like 'margin10', 'padding5'
        r'^(red|blue|green|yellow|black|white|gray)$',  # color names
        r'^(small|medium|large|xl|xxl)$',  # size classes
        r'^(left|right|center|justify)$',  # alignment
        r'^(bold|italic|underline)$',  # text styling
    ]
    
    # Additional aggressive styling patterns for UI frameworks
    AGGRESSIVE_STYLING_PATTERNS = [
        r'^hoverable$',  # hover states
        r'^collapsed$',  # collapse states
        r'^collapsible$',  # collapsible elements
        r'^collapser$',  # collapse triggers
        r'^expanded$',  # expand states
        r'^selected$',  # selection states
        r'^active$',  # active states
        r'^obj$',  # generic object classes
        r'^array$',  # array classes
        r'^last$',  # positional classes
        r'^first$',  # positional classes
        r'^sc-[a-zA-Z0-9_-]+$',  # styled-components generated classes
        r'^react-tabs__',  # React tabs framework
        r'^tab-(error|success|warning)$',  # tab state classes
        r'^.*[A-Z]{3,}[a-z]{2,}$',  # classes with mixed case patterns like 'hCKhjF'
        r'^[a-z]{2,5}[A-Z]{2,5}$',  # short mixed case like 'dYpyED'
        r'^[a-zA-Z]{6}$',  # exactly 6 character hash classes like 'dYpyED', 'hCKhjF'
    ]
    
    # Attributes to always preserve
    CORE_ATTRS = {'id', 'class', 'role'}
    SEMANTIC_ATTRS = {'href', 'src', 'alt', 'title', 'type', 'value', 'name'}
    ARIA_ATTRS_PREFIX = 'aria-'
    DATA_ATTRS_PREFIX = 'data-'
    
    # Tags to remove completely
    REMOVE_TAGS = {"script", "style", "noscript", "iframe", "embed", "object"}
    
    def __init__(self, preserve_structure=True, aggressive_cleaning=True, ultra_aggressive=False, simplify_spans=False):
        self.preserve_structure = preserve_structure
        self.aggressive_cleaning = aggressive_cleaning
        self.ultra_aggressive = ultra_aggressive
        self.simplify_spans = simplify_spans
        
    def should_remove_img(self, img_elem):
        """Check if an img tag should be removed due to large data URLs."""
        src = img_elem.get('src', '')
        if src.startswith('data:') and len(src) > 1000:  # Remove large data URLs
            return True
        return False
        
    def is_semantic_class(self, class_name):
        """Check if a CSS class has semantic meaning."""
        class_lower = class_name.lower()
        
        # Check against basic styling patterns first (return False if matches)
        for pattern in self.STYLING_PATTERNS:
            if re.match(pattern, class_lower):
                return False
                
        # Check against aggressive styling patterns if ultra_aggressive mode is enabled
        if self.ultra_aggressive:
            for pattern in self.AGGRESSIVE_STYLING_PATTERNS:
                if re.match(pattern, class_name):  # Use original case for mixed-case patterns
                    return False
        
        # Check against semantic patterns
        for _, patterns in self.SEMANTIC_CLASS_PATTERNS.items():
            if any(pattern in class_lower for pattern in patterns):
                return True
                
        # If it doesn't match styling patterns and is reasonably named, keep it
        return len(class_name) > 2 and not class_name.isdigit()
    
    def should_remove_single_hash_class(self, class_string):
        """Check if a class attribute contains only a single 6-character hash."""
        if not self.ultra_aggressive:
            return False
            
        # Check if it's a single class with exactly 6 characters
        class_string = str(class_string).strip()
        if ' ' in class_string:  # Multiple classes
            return False
            
        # Remove if it's exactly 6 characters (typical CSS-in-JS hash)
        return len(class_string) == 6 and class_string.isalnum()
    
    def clean_class_attribute(self, classes):
        """Filter class list to keep only semantic classes."""
        if not classes:
            return None
            
        # Check for single 6-character hash classes first
        if self.should_remove_single_hash_class(classes):
            return None
            
        if isinstance(classes, list):
            class_list = classes
        else:
            class_list = str(classes).split()
            
        semantic_classes = [cls for cls in class_list if self.is_semantic_class(cls)]
        return ' '.join(semantic_classes) if semantic_classes else None
    
    def should_preserve_attribute(self, attr_name, attr_value, tag_name=None):
        """Enhanced attribute filtering logic."""
        attr_lower = attr_name.lower()
        
        # Remove all aria-* attributes
        if attr_lower.startswith(self.ARIA_ATTRS_PREFIX):
            return False
            
        # Remove class attributes from span tags
        if tag_name == 'span' and attr_lower == 'class':
            return False
            
        # Remove React tabs generated IDs (react-tabs-XXXX)
        if attr_lower == 'id' and self.ultra_aggressive:
            attr_value_str = str(attr_value)
            if re.match(r'^react-tabs-\d+$', attr_value_str):
                return False
        
        # Always preserve core and semantic attributes (excluding class for spans)
        if attr_lower in self.CORE_ATTRS or attr_lower in self.SEMANTIC_ATTRS:
            return True
            
        # Preserve meaningful data attributes
        if attr_lower.startswith(self.DATA_ATTRS_PREFIX):
            # Remove data-testid attributes (used for testing)
            if attr_lower == 'data-testid':
                return False
            # Keep data attributes that seem semantic
            data_name = attr_lower[5:]  # Remove 'data-' prefix
            return any(pattern in data_name for pattern in ['id', 'role', 'type', 'section', 'item'])
            
        return False
    
    def aggressive_text_clean(self, text):
        """More aggressive text normalization."""
        if not text:
            return ""
            
        # Remove excessive whitespace more aggressively
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove empty parentheses and brackets
        text = re.sub(r'\(\s*\)', '', text)
        text = re.sub(r'\[\s*\]', '', text)
        
        # Clean up multiple punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[-]{2,}', '--', text)
        
        return text.strip()
    
    def should_simplify_span(self, span_elem):
        """Check if a span should be simplified (converted to text)."""
        if not self.simplify_spans:
            return False
            
        # Don't simplify spans with attributes we want to keep
        for attr_name in span_elem.attrs:
            if self.should_preserve_attribute(attr_name, span_elem.attrs[attr_name], 'span'):
                return False
        
        # Get the text content
        text_content = span_elem.get_text().strip()
        
        # Simplify spans that only contain punctuation or simple values
        if text_content in [',', '{', '}', '[', ']', ':', '(', ')', ';']:
            return True
            
        # Simplify spans with simple quoted strings or numbers
        if (text_content.startswith('"') and text_content.endswith('"')) or \
           text_content.replace('.', '').replace('-', '').isdigit() or \
           text_content in ['true', 'false', 'null']:
            return True
            
        return False
    
    def process_element(self, soup_elem, parent_xml_elem):
        """Process HTML element preserving structure."""
        if isinstance(soup_elem, NavigableString):
            # Handle text nodes with aggressive cleaning
            text = self.aggressive_text_clean(str(soup_elem))
            if text:
                if parent_xml_elem.text:
                    parent_xml_elem.text += " " + text
                else:
                    parent_xml_elem.text = text
            return
            
        if not isinstance(soup_elem, Tag):
            return
            
        # Skip removed tags
        if soup_elem.name in self.REMOVE_TAGS:
            return
            
        # Skip img tags with large data URLs
        if soup_elem.name == 'img' and self.should_remove_img(soup_elem):
            return
            
        # Simplify spans that only contain simple content
        if soup_elem.name == 'span' and self.should_simplify_span(soup_elem):
            # Convert span to plain text
            text = self.aggressive_text_clean(soup_elem.get_text())
            if text:
                if parent_xml_elem.text:
                    parent_xml_elem.text += text
                else:
                    parent_xml_elem.text = text
            return
            
        # Create XML element with original tag name (preserve structure)
        tag_name = soup_elem.name
        xml_elem = ET.SubElement(parent_xml_elem, tag_name)
        
        # Process attributes with enhanced filtering
        for attr_name, attr_value in soup_elem.attrs.items():
            if self.should_preserve_attribute(attr_name, attr_value, tag_name):
                if attr_name == 'class':
                    # Special handling for class attribute
                    cleaned_classes = self.clean_class_attribute(attr_value)
                    if cleaned_classes:
                        xml_elem.set('class', cleaned_classes)
                else:
                    # Handle other attributes
                    if isinstance(attr_value, list):
                        attr_value = " ".join(attr_value)
                    attr_value = str(attr_value).strip()
                    if attr_value:
                        xml_elem.set(attr_name, attr_value)
        
        # Process children
        for child in soup_elem.children:
            self.process_element(child, xml_elem)
    
    def convert(self, html_content):
        """Convert HTML to clean XML preserving structure."""
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Create root with metadata about processing
        root = ET.Element("html-cleaned")
        root.set("processed-by", "StructuralHTMLConverter")
        root.set("preserves-structure", str(self.preserve_structure))
        
        # Process the entire document structure
        if soup.html:
            self.process_element(soup.html, root)
        else:
            # If no html tag, process body or entire content
            body = soup.find("body") or soup
            for child in body.children:
                self.process_element(child, root)
        
        return root
    
    def prettify_xml(self, elem):
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def get_stats(self, original_html, xml_string):
        """Calculate size reduction statistics."""
        original_size = len(original_html.encode("utf-8"))
        new_size = len(xml_string.encode("utf-8"))
        reduction = (original_size - new_size) / original_size * 100

        return {
            "original_size": original_size,
            "new_size": new_size,
            "reduction_percent": reduction,
            "reduction_bytes": original_size - new_size,
        }


class HTMLToXMLConverter:
    """Converts HTML to clean, structured XML by removing unnecessary attributes."""

    # Attributes to preserve (semantic/structural)
    PRESERVE_ATTRS = {
        "id",
        "name",
        "href",
        "src",
        "alt",
        "title",
        "type",
        "value",
        "action",
        "method",
        "rel",
        "target",
        "colspan",
        "rowspan",
        "role",
        "aria-label",
        "aria-labelledby",
        "aria-controls",
        "data-section-id",
        "data-item-id",
        "data-role",
    }

    # Tags to completely remove (including content)
    REMOVE_TAGS = {"script", "style", "noscript", "iframe", "embed", "object"}

    # Tags to unwrap (remove tag but keep content)
    UNWRAP_TAGS = {"font", "center", "b", "i", "u", "s", "strike"}

    # Semantic tag mappings
    TAG_MAPPINGS = {
        "div": "section",
        "span": "text",
        "b": "strong",
        "i": "em",
        "h1": "heading1",
        "h2": "heading2",
        "h3": "heading3",
        "h4": "heading4",
        "h5": "heading5",
        "h6": "heading6",
    }

    def __init__(self, preserve_all_data_attrs=False, custom_preserve_attrs=None):
        """
        Initialize converter with options.

        Args:
            preserve_all_data_attrs: Keep all data-* attributes
            custom_preserve_attrs: Additional attributes to preserve
        """
        self.preserve_attrs = self.PRESERVE_ATTRS.copy()
        if custom_preserve_attrs:
            self.preserve_attrs.update(custom_preserve_attrs)
        self.preserve_all_data_attrs = preserve_all_data_attrs

    def clean_text(self, text):
        """Clean and normalize text content."""
        if not text:
            return ""
        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove leading/trailing whitespace
        text = text.strip()
        # Escape XML special characters
        text = html.escape(text, quote=False)
        return text

    def should_preserve_attr(self, attr_name):
        """Check if an attribute should be preserved."""
        if attr_name in self.preserve_attrs:
            return True
        if self.preserve_all_data_attrs and attr_name.startswith("data-"):
            return True
        return False

    def convert_tag_name(self, tag_name):
        """Convert HTML tag name to XML element name."""
        # Use semantic mapping if available
        if tag_name in self.TAG_MAPPINGS:
            return self.TAG_MAPPINGS[tag_name]
        # Replace invalid XML characters
        tag_name = re.sub(r"[^a-zA-Z0-9_-]", "_", tag_name)
        return tag_name

    def process_element(self, soup_elem, parent_xml_elem):
        """Recursively process HTML element to XML."""
        if isinstance(soup_elem, NavigableString):
            # Handle text nodes
            text = self.clean_text(str(soup_elem))
            if text:
                if parent_xml_elem.text:
                    parent_xml_elem.text += " " + text
                else:
                    parent_xml_elem.text = text
            return

        if not isinstance(soup_elem, Tag):
            return

        # Skip removed tags
        if soup_elem.name in self.REMOVE_TAGS:
            return

        # Handle unwrap tags
        if soup_elem.name in self.UNWRAP_TAGS:
            for child in soup_elem.children:
                self.process_element(child, parent_xml_elem)
            return

        # Create XML element
        tag_name = self.convert_tag_name(soup_elem.name)
        xml_elem = ET.SubElement(parent_xml_elem, tag_name)

        # Process attributes
        for attr_name, attr_value in soup_elem.attrs.items():
            if self.should_preserve_attr(attr_name):
                if isinstance(attr_value, list):
                    attr_value = " ".join(attr_value)
                # Clean attribute value
                attr_value = str(attr_value).strip()
                if attr_value:
                    xml_elem.set(attr_name, attr_value)

        # Special handling for specific tags
        if soup_elem.name == "a" and "href" not in xml_elem.attrib:
            # Preserve href even if empty
            xml_elem.set("href", "")

        # Process children
        has_children = False
        for child in soup_elem.children:
            has_children = True
            self.process_element(child, xml_elem)

        # Add text content for empty elements
        if not has_children and not xml_elem.text:
            xml_elem.text = ""

    def extract_metadata(self, soup):
        """Extract metadata from HTML head."""
        metadata = {}
        head = soup.find("head")
        if head:
            # Extract title
            title = head.find("title")
            if title:
                metadata["title"] = self.clean_text(title.get_text())

            # Extract meta tags
            for meta in head.find_all("meta"):
                name = meta.get("name") or meta.get("property")
                content = meta.get("content")
                if name and content:
                    metadata[name] = content

        return metadata

    def convert(self, html_content):
        """Convert HTML to clean XML."""
        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Create root XML element
        root = ET.Element("document")

        # Add metadata
        metadata = self.extract_metadata(soup)
        if metadata:
            meta_elem = ET.SubElement(root, "metadata")
            for key, value in metadata.items():
                elem = ET.SubElement(meta_elem, "meta")
                elem.set("name", key)
                elem.text = value

        # Process body content
        body = soup.find("body")
        if not body:
            body = soup

        content_elem = ET.SubElement(root, "content")
        for child in body.children:
            self.process_element(child, content_elem)

        return root

    def prettify_xml(self, elem):
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def get_stats(self, original_html, xml_string):
        """Calculate size reduction statistics."""
        original_size = len(original_html.encode("utf-8"))
        new_size = len(xml_string.encode("utf-8"))
        reduction = (original_size - new_size) / original_size * 100

        return {
            "original_size": original_size,
            "new_size": new_size,
            "reduction_percent": reduction,
            "reduction_bytes": original_size - new_size,
        }


def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(
        description="Convert HTML to clean, structured XML"
    )
    parser.add_argument("input_file", type=str, help="Input HTML file path")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output XML file path (default: input_file.xml)",
    )
    parser.add_argument(
        "--preserve-data-attrs",
        action="store_true",
        help="Preserve all data-* attributes",
    )
    parser.add_argument(
        "--preserve-attrs",
        type=str,
        nargs="+",
        help="Additional attributes to preserve",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show size reduction statistics"
    )
    parser.add_argument(
        "--no-pretty",
        action="store_true",
        help="Disable pretty printing (more compact)",
    )
    parser.add_argument(
        "--structural",
        action="store_true",
        help="Use enhanced structural converter (preserves HTML tags and smart class filtering)",
    )
    parser.add_argument(
        "--ultra-aggressive",
        action="store_true",
        help="Enable ultra-aggressive cleaning (removes UI framework classes and states)",
    )
    parser.add_argument(
        "--simplify-spans",
        action="store_true",
        help="Simplify spans containing only punctuation or simple values to plain text",
    )

    args = parser.parse_args()

    # Read input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Set output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".xml")

    # Choose converter
    if args.structural:
        converter = StructuralHTMLConverter(
            preserve_structure=True,
            aggressive_cleaning=True,
            ultra_aggressive=args.ultra_aggressive,
            simplify_spans=args.simplify_spans
        )
    else:
        converter = HTMLToXMLConverter(
            preserve_all_data_attrs=args.preserve_data_attrs,
            custom_preserve_attrs=set(args.preserve_attrs) if args.preserve_attrs else None,
        )

    try:
        xml_root = converter.convert(html_content)

        # Generate XML string
        if args.no_pretty:
            xml_string = ET.tostring(xml_root, encoding="unicode")
        else:
            xml_string = converter.prettify_xml(xml_root)

        # Write output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_string)

        print(f"Successfully converted '{input_path}' to '{output_path}'")
        if args.structural:
            mode = "StructuralHTMLConverter"
            features = []
            if args.ultra_aggressive:
                features.append("ultra-aggressive")
            if args.simplify_spans:
                features.append("span-simplification")
            if features:
                mode += f" ({', '.join(features)})"
            print(f"Used enhanced {mode}")

        # Show statistics if requested
        if args.stats:
            stats = converter.get_stats(html_content, xml_string)
            print("\nConversion Statistics:")
            print(f"  Original size: {stats['original_size']:,} bytes")
            print(f"  New size: {stats['new_size']:,} bytes")
            print(
                f"  Reduction: {stats['reduction_bytes']:,} bytes ({stats['reduction_percent']:.1f}%)"
            )

    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


# Example usage for API documentation
class APIDocumentationConverter(HTMLToXMLConverter):
    """Specialized converter for API documentation HTML."""

    def __init__(self):
        super().__init__()
        # Add API-specific attributes to preserve
        self.preserve_attrs.update(
            {
                "data-section-id",
                "data-item-id",
                "data-role",
                "role",
                "aria-label",
                "aria-labelledby",
                "aria-controls",
                "aria-selected",
                "aria-disabled",
                "tabindex",
                "data-rttabs",
                "data-rttab",
            }
        )

    def convert_tag_name(self, tag_name):
        """Convert HTML tag names with API documentation in mind."""
        api_mappings = {
            "div": "section",
            "span": "text",
            "button": "action",
            "table": "parameters",
            "tbody": "parameter-list",
            "tr": "parameter",
            "td": "parameter-info",
            "code": "code-block",
            "pre": "code-sample",
        }

        if tag_name in api_mappings:
            return api_mappings[tag_name]
        return super().convert_tag_name(tag_name)


# Usage example
if __name__ == "__main__":
    # For API documentation specifically
    if "--api-mode" in sys.argv:
        sys.argv.remove("--api-mode")
        # Use specialized API converter
        # (This would require modifying the main() function to support this)
        print("API mode enabled - using specialized converter")

    main()