import React, { useState } from "react";

// A recursive component to display the trie node and its children
const TrieNode = ({ node, depth = 0, isLastChild = false }) => {
    const [collapsed, setCollapsed] = useState(false);
    const paddingLeft = `${depth * 20}px`;
    const isRoot = node.name === "root";
    const hasChildren = node.children && node.children.length > 0;
    
    const toggleCollapse = (e) => {
        e.stopPropagation();
        if (hasChildren) {
            setCollapsed(!collapsed);
        }
    };
    
    return (
        <div className="font-mono text-sm">
            <div 
                style={{ paddingLeft }} 
                className={`py-1.5 flex items-center ${isRoot ? 'text-purple-300 font-bold' : 'text-blue-300'} 
                ${hasChildren ? 'cursor-pointer hover:bg-gray-800/50 rounded' : ''}`}
                onClick={toggleCollapse}
            >
                {!isRoot && (
                    <span className="mr-2 font-mono text-gray-400">
                        {isLastChild ? '└─' : '├─'}
                    </span>
                )}
                
                {hasChildren && (
                    <span className="w-4 mr-1 text-gray-400">
                        {collapsed ? '▶' : '▼'}
                    </span>
                )}
                
                {!hasChildren && <span className="w-4"></span>}
                
                <span className="transition-all duration-200 hover:text-blue-200">
                    {node.name}
                </span>
                
                {node.attributes && node.attributes.ip && (
                    <span className="ml-2 px-2 py-0.5 bg-green-900/70 text-green-300 rounded-md text-xs border border-green-800 shadow-sm">
                        {node.attributes.ip}
                    </span>
                )}
                
                {node.attributes && node.attributes.isEnd && !node.attributes.ip && (
                    <span className="ml-2 px-2 py-0.5 bg-yellow-900/70 text-yellow-300 rounded-md text-xs border border-yellow-800 shadow-sm">
                        end
                    </span>
                )}
            </div>
            
            {!collapsed && node.children && node.children.map((child, index) => (
                <TrieNode 
                    key={`${child.name}-${index}`} 
                    node={child} 
                    depth={depth + 1} 
                    isLastChild={index === node.children.length - 1}
                />
            ))}
        </div>
    );
};

const TrieVisualization = ({ data }) => {
    if (!data) return (
        <div className="flex items-center justify-center h-32 text-gray-400">
            No trie data available
        </div>
    );
    
    return (
        <div className="trie-visualization">
            <div className="mb-2 text-xs text-gray-400">
                Click on nodes with children to expand/collapse
            </div>
            <TrieNode node={data} />
        </div>
    );
};

export default TrieVisualization;
