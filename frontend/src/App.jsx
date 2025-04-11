/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react";
import axios from "axios";
import TrieVisualization from "./components/TrieVisualization";

function App() {
    const [domain, setDomain] = useState("");
    const [ip, setIp] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [trieData, setTrieData] = useState(null);
    const [showTrie, setShowTrie] = useState(false);
    const [history, setHistory] = useState([]);

    // Fetch trie structure on initial load and after resolution
    const fetchTrieStructure = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/trie');
            setTrieData(response.data);
        } catch (err) {
            console.error("Failed to fetch trie structure:", err);
        }
    };

    // Load trie data on component mount
    useEffect(() => {
        fetchTrieStructure();
    }, []);

    const resolveDomain = async () => {
        if (!domain.trim()) return;
        
        setIp(null);
        setError(null);
        setLoading(true);
        
        try {
            const response = await axios.get(`http://127.0.0.1:5000/resolve?domain=${domain}`);
            setIp(response.data.ip);
            
            // Add to history
            setHistory(prev => [
                { domain, ip: response.data.ip, timestamp: new Date().toLocaleTimeString() },
                ...prev.slice(0, 4) // Keep last 5 entries
            ]);
            
            // If it's a newly generated IP, show a note
            if (response.data.note) {
                setError(`New domain detected. Fetched actual IP address`);
            }
            
            // Refresh trie structure after resolution
            await fetchTrieStructure();
            
            // Auto-show trie after resolving
            setShowTrie(true);
        } catch (err) {
            setError("Server error occurred.");
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            resolveDomain();
        }
    };

    const handleHistoryClick = (historyDomain) => {
        setDomain(historyDomain);
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-b from-slate-900 via-gray-900 to-gray-800">
            <div className="w-full max-w-5xl p-6 border border-gray-700 shadow-2xl bg-gray-800/90 backdrop-blur-sm rounded-xl">
                <div className="flex flex-col items-center mb-8">
                    <h1 className="mb-2 text-4xl font-bold text-transparent bg-blue-400 bg-clip-text">DNS Resolver</h1>
                    <p className="text-sm text-gray-400">Fast domain resolution with compressed trie data structure</p>
                </div>
                
                <div className="mb-8">
                    <div className="relative flex gap-2">
                        <div className="relative w-full group">
                            <div className="absolute inset-0 transition duration-200 rounded-lg opacity-25 bg-gradient-to-r from-blue-500 to-purple-600 blur group-hover:opacity-40"></div>
                            <input 
                                type="text" 
                                placeholder="Enter domain (e.g., google.com)" 
                                value={domain} 
                                onChange={(e) => setDomain(e.target.value)}
                                onKeyDown={handleKeyDown}
                                className="relative w-full px-4 py-3 text-gray-100 placeholder-gray-400 border border-gray-600 rounded-lg bg-gray-700/90 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>
                        <button 
                            onClick={resolveDomain}
                            disabled={loading || !domain.trim()}
                            className="px-6 py-3 font-medium text-gray-100 transition-all duration-200 rounded-lg shadow-md bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? (
                                <div className="flex items-center">
                                    <svg className="w-4 h-4 mr-2 -ml-1 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Resolving...
                                </div>
                            ) : 'Resolve'}
                        </button>
                    </div>
                </div>
                
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                    <div className="space-y-4">
                        {ip && (
                            <div className="p-4 transition-all transform border rounded-lg shadow-lg bg-gray-700/80 border-green-700/70">
                                <h2 className="flex items-center text-lg font-medium text-green-400">
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                                    </svg>
                                    IP Address:
                                </h2>
                                <p className="mt-1 font-mono text-xl text-green-300">{ip}</p>
                                {/* <p className="mt-2 text-xs text-gray-400">Domain: {domain}</p> */}
                            </div>
                        )}
                        
                        {error && (
                            <div className="p-4 border rounded-lg shadow-lg bg-gray-700/80 border-yellow-600/70">
                                <h2 className="flex items-center text-lg font-medium text-yellow-400">
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    Note:
                                </h2>
                                <p className="text-yellow-300">{error}</p>
                            </div>
                        )}
                    </div>
                    
                    <div className="space-y-2">
                        <div className="flex items-center justify-between mb-2">
                            <h2 className="flex items-center text-lg font-medium text-purple-400">
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"></path>
                                </svg>
                                Compressed Trie Structure:
                            </h2>
                            <button 
                                onClick={() => setShowTrie(!showTrie)}
                                className="px-3 py-1 text-xs text-gray-300 transition-all transform bg-gray-700 rounded-full shadow-md hover:bg-gray-600 hover:scale-105 focus:outline-none focus:ring-1 focus:ring-purple-500"
                            >
                                {showTrie ? 'Hide Trie' : 'Show Trie'}
                            </button>
                        </div>
                        
                        {showTrie && trieData && (
                            <div className="p-4 overflow-auto bg-gray-700/80 border border-purple-700/50 rounded-lg max-h-[400px] shadow-lg">
                                <TrieVisualization data={trieData} />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
