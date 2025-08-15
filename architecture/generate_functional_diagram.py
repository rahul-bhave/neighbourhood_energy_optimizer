#!/usr/bin/env python3
"""
Functional Specification Diagram Generator
Generates a visual representation of the Neighbourhood Energy Optimizer business flow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_functional_diagram():
    """Create the functional specification diagram"""
    
    # Set up the figure
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Colors
    colors = {
        'start': '#E8F5E8',
        'process': '#E6F3FF',
        'decision': '#FFF2E6',
        'output': '#F0E6FF',
        'data': '#FFE6E6',
        'border': '#333333'
    }
    
    # Title
    ax.text(8, 11.5, 'Neighbourhood Energy Optimizer - Functional Flow', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Start
    start_box = FancyBboxPatch((7, 10), 2, 1, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['start'], 
                              edgecolor=colors['border'], 
                              linewidth=2)
    ax.add_patch(start_box)
    ax.text(8, 10.5, 'START\nSystem Initialization', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    
    # Mock Data Generation
    data_box = FancyBboxPatch((1, 8.5), 3, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['data'], 
                             edgecolor=colors['border'], 
                             linewidth=2)
    ax.add_patch(data_box)
    ax.text(2.5, 9.25, 'Generate Mock Data\n(50 consumers)', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(2.5, 8.8, '• 5 consumers: 10% discount\n• 5 consumers: 5% (efficient)\n• 5 consumers: 5% (solar)\n• 5 consumers: no discount\n• 30 consumers: high usage', 
            fontsize=8, ha='center', va='center')
    
    # Monitor Agent
    monitor_box = FancyBboxPatch((6, 8.5), 3, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['process'], 
                                edgecolor=colors['border'], 
                                linewidth=2)
    ax.add_patch(monitor_box)
    ax.text(7.5, 9.25, 'Monitor Agent\nProcesses Consumers', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(7.5, 8.8, '• Retrieves consumer data\n• Sends one consumer at a time\n• Waits for acknowledgment', 
            fontsize=8, ha='center', va='center')
    
    # Incentives Agent
    incentives_box = FancyBboxPatch((11, 8.5), 3, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=colors['process'], 
                                   edgecolor=colors['border'], 
                                   linewidth=2)
    ax.add_patch(incentives_box)
    ax.text(12.5, 9.25, 'Incentives Agent\nAnalyzes Eligibility', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(12.5, 8.8, '• Receives consumer data\n• Determines discount scenario\n• Generates notification', 
            fontsize=8, ha='center', va='center')
    
    # Decision Points
    decision1_box = FancyBboxPatch((1, 6.5), 4, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['decision'], 
                                  edgecolor=colors['border'], 
                                  linewidth=2)
    ax.add_patch(decision1_box)
    ax.text(3, 7.25, 'Usage Analysis\n(< 4 kWh/day?)', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    
    decision2_box = FancyBboxPatch((7, 6.5), 4, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['decision'], 
                                  edgecolor=colors['border'], 
                                  linewidth=2)
    ax.add_patch(decision2_box)
    ax.text(9, 7.25, 'Equipment & Solar\nAnalysis', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Discount Scenarios
    scenario1_box = FancyBboxPatch((1, 4.5), 3, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['output'], 
                                  edgecolor=colors['border'], 
                                  linewidth=2)
    ax.add_patch(scenario1_box)
    ax.text(2.5, 5.25, '10% Discount\nEligible', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(2.5, 4.9, '• < 4 kWh/day\n• Efficient equipment\n• Solar production', 
            fontsize=8, ha='center', va='center')
    
    scenario2_box = FancyBboxPatch((5.5, 4.5), 3, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['output'], 
                                  edgecolor=colors['border'], 
                                  linewidth=2)
    ax.add_patch(scenario2_box)
    ax.text(7, 5.25, '5% Discount\nEligible', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(7, 4.9, '• < 4 kWh/day\n• Efficient equipment\n• OR Solar production', 
            fontsize=8, ha='center', va='center')
    
    scenario3_box = FancyBboxPatch((10, 4.5), 3, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['output'], 
                                  edgecolor=colors['border'], 
                                  linewidth=2)
    ax.add_patch(scenario3_box)
    ax.text(11.5, 5.25, 'No Discount\nEligible', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(11.5, 4.9, '• < 4 kWh/day\n• No efficient equipment\n• No solar production', 
            fontsize=8, ha='center', va='center')
    
    scenario4_box = FancyBboxPatch((13.5, 4.5), 2, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['output'], 
                                  edgecolor=colors['border'], 
                                  linewidth=2)
    ax.add_patch(scenario4_box)
    ax.text(14.5, 5.25, 'High Usage\n(≥ 4 kWh/day)', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(14.5, 4.9, '• ≥ 4 kWh/day\n• Encouragement\n• Recommendations', 
            fontsize=8, ha='center', va='center')
    
    # LLM Processing
    llm_box = FancyBboxPatch((1, 2.5), 4, 1.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['process'], 
                            edgecolor=colors['border'], 
                            linewidth=2)
    ax.add_patch(llm_box)
    ax.text(3, 3.25, 'LLM Processing\n(WatsonX/Mock)', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(3, 2.9, '• Generates personalized\n• notifications\n• Fallback templates', 
            fontsize=8, ha='center', va='center')
    
    # Notification Output
    output_box = FancyBboxPatch((7, 2.5), 4, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['output'], 
                               edgecolor=colors['border'], 
                               linewidth=2)
    ax.add_patch(output_box)
    ax.text(9, 3.25, 'Notification Output\n(Detailed Messages)', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(9, 2.9, '• Personalized content\n• Discount information\n• Actionable advice', 
            fontsize=8, ha='center', va='center')
    
    # Acknowledgment
    ack_box = FancyBboxPatch((13, 2.5), 2.5, 1.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['process'], 
                            edgecolor=colors['border'], 
                            linewidth=2)
    ax.add_patch(ack_box)
    ax.text(14.25, 3.25, 'Send\nAcknowledgment', 
            fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(14.25, 2.9, '• Confirm processing\n• Ready for next\n• consumer', 
            fontsize=8, ha='center', va='center')
    
    # End
    end_box = FancyBboxPatch((7, 0.5), 2, 1, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['start'], 
                            edgecolor=colors['border'], 
                            linewidth=2)
    ax.add_patch(end_box)
    ax.text(8, 1, 'END\nAll Consumers\nProcessed', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    
    # Connections
    # Start to Data Generation
    con1 = ConnectionPatch((8, 10), (2.5, 10), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con1)
    
    # Data to Monitor
    con2 = ConnectionPatch((4, 9.25), (6, 9.25), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con2)
    
    # Monitor to Incentives
    con3 = ConnectionPatch((9, 9.25), (11, 9.25), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con3)
    ax.text(10, 9.5, 'Consumer Data', fontsize=8, ha='center')
    
    # Incentives to Decision 1
    con4 = ConnectionPatch((12.5, 8), (3, 8), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con4)
    
    # Decision 1 to Decision 2
    con5 = ConnectionPatch((3, 6.5), (7, 6.5), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con5)
    ax.text(5, 6.3, 'Low Usage', fontsize=8, ha='center')
    
    # Decision 2 to Scenarios
    con6 = ConnectionPatch((9, 6.5), (2.5, 6), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con6)
    ax.text(6, 6.3, 'Both', fontsize=8, ha='center')
    
    con7 = ConnectionPatch((9, 6.5), (7, 6), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con7)
    ax.text(8, 6.3, 'One', fontsize=8, ha='center')
    
    con8 = ConnectionPatch((9, 6.5), (11.5, 6), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con8)
    ax.text(10.5, 6.3, 'None', fontsize=8, ha='center')
    
    # Decision 1 to High Usage
    con9 = ConnectionPatch((3, 6.5), (14.5, 6), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['border'])
    ax.add_patch(con9)
    ax.text(9, 5.5, 'High Usage', fontsize=8, ha='center')
    
    # Scenarios to LLM
    con10 = ConnectionPatch((2.5, 4.5), (3, 4), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con10)
    
    con11 = ConnectionPatch((7, 4.5), (3, 4), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con11)
    
    con12 = ConnectionPatch((11.5, 4.5), (3, 4), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con12)
    
    con13 = ConnectionPatch((14.5, 4.5), (3, 4), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con13)
    
    # LLM to Output
    con14 = ConnectionPatch((5, 3.25), (7, 3.25), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con14)
    
    # Output to Acknowledgment
    con15 = ConnectionPatch((11, 3.25), (13, 3.25), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con15)
    
    # Acknowledgment back to Monitor (loop)
    con16 = ConnectionPatch((14.25, 2.5), (7.5, 7), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con16)
    ax.text(11, 4.5, 'Next Consumer', fontsize=8, ha='center')
    
    # Acknowledgment to End
    con17 = ConnectionPatch((14.25, 2.5), (8, 1.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc=colors['border'])
    ax.add_patch(con17)
    ax.text(12, 1.8, 'All Complete', fontsize=8, ha='center')
    
    # Flow labels
    ax.text(0.5, 9.5, 'Data Layer', fontsize=14, fontweight='bold', rotation=90)
    ax.text(0.5, 7, 'Processing Layer', fontsize=14, fontweight='bold', rotation=90)
    ax.text(0.5, 5, 'Decision Layer', fontsize=14, fontweight='bold', rotation=90)
    ax.text(0.5, 3, 'Output Layer', fontsize=14, fontweight='bold', rotation=90)
    
    plt.tight_layout()
    return fig

def save_functional_diagram(filename='functional_specification.png'):
    """Generate and save the functional diagram"""
    fig = create_functional_diagram()
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Functional specification diagram saved as {filename}")

if __name__ == '__main__':
    save_functional_diagram()



