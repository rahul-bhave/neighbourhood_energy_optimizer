#!/usr/bin/env python3
"""
Technical Architecture Diagram Generator
Generates a visual representation of the Neighbourhood Energy Optimizer system architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Create the technical architecture diagram"""
    
    # Set up the figure
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Colors
    colors = {
        'database': '#FFE6E6',
        'mcp': '#E6F3FF',
        'agent': '#E6FFE6',
        'framework': '#FFF2E6',
        'communication': '#F0E6FF',
        'border': '#333333'
    }
    
    # Title
    ax.text(8, 11.5, 'Neighbourhood Energy Optimizer - Technical Architecture', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Database Layer
    db_box = FancyBboxPatch((1, 1), 3, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['database'], 
                           edgecolor=colors['border'], 
                           linewidth=2)
    ax.add_patch(db_box)
    ax.text(2.5, 1.75, 'SQLite Database\n(mock_data.db)', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    
    # MCP Layer
    mcp_server_box = FancyBboxPatch((6, 1), 3, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=colors['mcp'], 
                                   edgecolor=colors['border'], 
                                   linewidth=2)
    ax.add_patch(mcp_server_box)
    ax.text(7.5, 1.75, 'MCP Server\n(mcp_server.py)', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    
    mcp_client_box = FancyBboxPatch((6, 3), 3, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=colors['mcp'], 
                                   edgecolor=colors['border'], 
                                   linewidth=2)
    ax.add_patch(mcp_client_box)
    ax.text(7.5, 3.75, 'MCP Client\n(mcp_client.py)', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    
    # BeeAI Framework Layer
    framework_box = FancyBboxPatch((1, 5), 8, 2, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['framework'], 
                                  edgecolor=colors['border'], 
                                  linewidth=2)
    ax.add_patch(framework_box)
    ax.text(5, 6.5, 'BeeAI Framework', 
            fontsize=14, fontweight='bold', ha='center', va='center')
    ax.text(5, 6, '• BaseAgent\n• Emitter\n• Memory\n• Agent Communication', 
            fontsize=10, ha='center', va='center')
    
    # Agents Layer
    monitor_box = FancyBboxPatch((1, 8), 3, 2, 
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['agent'], 
                                edgecolor=colors['border'], 
                                linewidth=2)
    ax.add_patch(monitor_box)
    ax.text(2.5, 9.5, 'Energy Monitor\nAgent', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(2.5, 9, '• Monitors consumption\n• Sends consumer data\n• Tracks progress', 
            fontsize=9, ha='center', va='center')
    
    incentives_box = FancyBboxPatch((6, 8), 3, 2, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=colors['agent'], 
                                   edgecolor=colors['border'], 
                                   linewidth=2)
    ax.add_patch(incentives_box)
    ax.text(7.5, 9.5, 'Incentives Agent', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(7.5, 9, '• Analyzes eligibility\n• Generates notifications\n• Sends acknowledgments', 
            fontsize=9, ha='center', va='center')
    
    # LLM Layer
    llm_box = FancyBboxPatch((11, 8), 3, 2, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['communication'], 
                            edgecolor=colors['border'], 
                            linewidth=2)
    ax.add_patch(llm_box)
    ax.text(12.5, 9.5, 'LLM Service\n(WatsonX/Mock)', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(12.5, 9, '• Generates personalized\n• notifications\n• Fallback templates', 
            fontsize=9, ha='center', va='center')
    
    # Communication Layer
    emitter_box = FancyBboxPatch((11, 5), 3, 2, 
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['communication'], 
                                edgecolor=colors['border'], 
                                linewidth=2)
    ax.add_patch(emitter_box)
    ax.text(12.5, 6.5, 'Emitter\n(Agent Communication)', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(12.5, 6, '• Event-driven\n• Inter-agent messaging\n• Acknowledgment system', 
            fontsize=9, ha='center', va='center')
    
    # Main Application
    main_box = FancyBboxPatch((11, 1), 3, 2, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['framework'], 
                             edgecolor=colors['border'], 
                             linewidth=2)
    ax.add_patch(main_box)
    ax.text(12.5, 2.5, 'Main Application\n(src/main.py)', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(12.5, 2, '• Orchestrates agents\n• Manages lifecycle', 
            fontsize=9, ha='center', va='center')
    
    # Connections
    # Database to MCP Server
    con1 = ConnectionPatch((4, 1.75), (6, 1.75), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con1)
    ax.text(5, 1.5, 'SQL Queries', fontsize=8, ha='center')
    
    # MCP Server to Client
    con2 = ConnectionPatch((7.5, 2.5), (7.5, 3), "data", "data",
                          arrowstyle="<->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con2)
    ax.text(8.5, 2.75, 'JSON-RPC', fontsize=8, ha='center')
    
    # MCP Client to Framework
    con3 = ConnectionPatch((7.5, 4.5), (5, 5), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con3)
    ax.text(6.5, 4.8, 'Data Access', fontsize=8, ha='center')
    
    # Framework to Agents
    con4 = ConnectionPatch((5, 7), (2.5, 8), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con4)
    con5 = ConnectionPatch((5, 7), (7.5, 8), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con5)
    ax.text(5, 7.5, 'Agent Management', fontsize=8, ha='center')
    
    # Agents to Emitter
    con6 = ConnectionPatch((4, 9), (11, 6), "data", "data",
                          arrowstyle="<->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con6)
    con7 = ConnectionPatch((9, 9), (11, 6), "data", "data",
                          arrowstyle="<->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con7)
    ax.text(7.5, 7.5, 'Event Communication', fontsize=8, ha='center')
    
    # Incentives to LLM
    con8 = ConnectionPatch((9, 8.5), (11, 8.5), "data", "data",
                          arrowstyle="<->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con8)
    ax.text(10, 8.2, 'LLM Requests', fontsize=8, ha='center')
    
    # Main to Framework
    con9 = ConnectionPatch((11, 3), (9, 5), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con9)
    ax.text(10, 4, 'Orchestration', fontsize=8, ha='center')
    
    # Layer labels
    ax.text(0.5, 10.5, 'Application Layer', fontsize=14, fontweight='bold', rotation=90)
    ax.text(0.5, 7, 'Framework Layer', fontsize=14, fontweight='bold', rotation=90)
    ax.text(0.5, 3.5, 'Communication Layer', fontsize=14, fontweight='bold', rotation=90)
    ax.text(0.5, 1.5, 'Data Layer', fontsize=14, fontweight='bold', rotation=90)
    
    plt.tight_layout()
    return fig

def save_architecture_diagram(filename='technical_architecture.png'):
    """Generate and save the architecture diagram"""
    fig = create_architecture_diagram()
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Technical architecture diagram saved as {filename}")

if __name__ == '__main__':
    save_architecture_diagram()
