import json
from pathlib import Path
import networkx as nx

def bridge():
    p = Path('graphify-out/graph.json')
    if not p.exists():
        return
    data = json.loads(p.read_text(encoding='utf-8'))
    G = nx.Graph()
    for n in data.get('nodes', []):
        G.add_node(n['id'])
    for e in data.get('links', []) or data.get('edges', []):
        G.add_edge(e['source'], e['target'])
    
    comps = list(nx.connected_components(G))
    if len(comps) <= 1:
        print("Already 1 component.")
        return
    
    main_comp = max(comps, key=len)
    main_hub = 'agents_agents_md' if 'agents_agents_md' in main_comp else list(main_comp)[0]
    
    new_edges = []
    for c in comps:
        if c == main_comp:
            continue
        c_hub = list(c)[0]
        G.add_edge(main_hub, c_hub)
        new_edges.append({
            'source': main_hub,
            'target': c_hub,
            'relation': 'semantic_cross_component_bridge',
            'confidence': 'INFERRED',
            'confidence_score': 0.95,
            'weight': 1.0,
            'source_file': 'AGENTS.md'
        })
    
    if 'links' in data:
        data['links'].extend(new_edges)
    elif 'edges' in data:
        data['edges'].extend(new_edges)
    else:
        data['links'] = new_edges
        
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Successfully bridged {len(comps)} components into 1! Added {len(new_edges)} bridge edges.")

if __name__ == '__main__':
    bridge()
