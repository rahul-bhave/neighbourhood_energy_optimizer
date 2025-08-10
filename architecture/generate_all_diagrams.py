#!/usr/bin/env python3
"""
Generate All Diagrams Script
Generates both technical architecture and functional specification diagrams
"""

import os
import sys

# Add the parent directory to the path to import the diagram generators
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from architecture.generate_architecture_diagram import save_architecture_diagram
from architecture.generate_functional_diagram import save_functional_diagram

def generate_all_diagrams():
    """Generate both architecture and functional diagrams"""
    
    print("Generating Neighbourhood Energy Optimizer Diagrams...")
    print("=" * 50)
    
    # Create output directory if it doesn't exist
    output_dir = "architecture/diagrams"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate technical architecture diagram
    print("1. Generating Technical Architecture Diagram...")
    save_architecture_diagram(f"{output_dir}/technical_architecture.png")
    
    # Generate functional specification diagram
    print("2. Generating Functional Specification Diagram...")
    save_functional_diagram(f"{output_dir}/functional_specification.png")
    
    print("\n" + "=" * 50)
    print("✅ All diagrams generated successfully!")
    print(f"📁 Diagrams saved in: {output_dir}/")
    print("   - technical_architecture.png")
    print("   - functional_specification.png")
    print("\n📋 Diagram Descriptions:")
    print("   • Technical Architecture: Shows system components, layers, and connections")
    print("   • Functional Specification: Shows business flow and decision logic")

if __name__ == '__main__':
    generate_all_diagrams()
