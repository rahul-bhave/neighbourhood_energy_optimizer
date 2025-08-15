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

# ANSI Color Codes for colorful output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text, color=Colors.ENDC):
    """Print text with color"""
    print(f"{color}{text}{Colors.ENDC}")

def generate_all_diagrams():
    """Generate both architecture and functional diagrams"""
    
    print_colored("🏗️  Generating Neighbourhood Energy Optimizer Diagrams...", Colors.HEADER + Colors.BOLD)
    print_colored("=" * 60, Colors.OKBLUE)
    
    # Create output directory if it doesn't exist
    output_dir = "architecture/diagrams"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate technical architecture diagram
    print_colored("📊 1. Generating Technical Architecture Diagram...", Colors.OKCYAN + Colors.BOLD)
    save_architecture_diagram(f"{output_dir}/technical_architecture.png")
    print_colored("   ✅ Technical architecture diagram completed!", Colors.OKGREEN)
    
    # Generate functional specification diagram
    print_colored("🔄 2. Generating Functional Specification Diagram...", Colors.OKCYAN + Colors.BOLD)
    save_functional_diagram(f"{output_dir}/functional_specification.png")
    print_colored("   ✅ Functional specification diagram completed!", Colors.OKGREEN)
    
    print_colored("\n" + "=" * 60, Colors.OKBLUE)
    print_colored("🎉 All diagrams generated successfully!", Colors.OKGREEN + Colors.BOLD)
    print_colored(f"📁 Diagrams saved in: {Colors.UNDERLINE}{output_dir}/{Colors.ENDC}", Colors.OKBLUE)
    print_colored("   📋 technical_architecture.png", Colors.OKCYAN)
    print_colored("   📋 functional_specification.png", Colors.OKCYAN)
    print_colored("\n📖 Diagram Descriptions:", Colors.HEADER + Colors.BOLD)
    print_colored("   • Technical Architecture: Shows system components, layers, and connections", Colors.WARNING)
    print_colored("   • Functional Specification: Shows business flow and decision logic", Colors.WARNING)
    print_colored("\n🚀 You can now view the diagrams in the architecture/diagrams/ folder!", Colors.OKGREEN)

if __name__ == '__main__':
    generate_all_diagrams()



