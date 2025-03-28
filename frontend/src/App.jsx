/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import axios from "axios";

function App() {
    const [domain, setDomain] = useState("");
    const [ip, setIp] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const resolveDomain = async () => {
        if (!domain.trim()) return;
        
        setIp(null);
        setError(null);
        setLoading(true);
        
        try {
            const response = await axios.get(`http://127.0.0.1:5000/resolve?domain=${domain}`);
            setIp(response.data.ip);
            
            // If it's a newly generated IP, show a note
            if (response.data.note) {
                setError(`New domain detected. Generated random IP address.`);
            }
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

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex flex-col items-center justify-center p-4">
            <div className="bg-gray-800 rounded-xl shadow-lg p-6 w-full max-w-md border border-gray-700">
                <h1 className="text-3xl font-bold text-gray-100 mb-6 text-center">DNS Resolver</h1>
                
                <div className="mb-6">
                    <div className="flex gap-2">
                        <input 
                            type="text" 
                            placeholder="Enter domain (e.g., google.com)" 
                            value={domain} 
                            onChange={(e) => setDomain(e.target.value)}
                            onKeyDown={handleKeyDown}
                            className="w-full px-4 py-2 rounded-lg border border-gray-600 bg-gray-700 text-gray-100 placeholder-gray-400 
                            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <button 
                            onClick={resolveDomain}
                            disabled={loading || !domain.trim()}
                            className="px-4 py-2 bg-blue-600 text-gray-100 rounded-lg hover:bg-blue-700 transition-colors 
                            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800 
                            disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Loading...' : 'Resolve'}
                        </button>
                    </div>
                </div>
                
                {ip && (
                    <div className="p-4 bg-gray-700 rounded-lg border border-green-700">
                        <h2 className="text-lg font-medium text-green-400">IP Address:</h2>
                        <p className="text-xl font-mono text-green-300 mt-1">{ip}</p>
                    </div>
                )}
                
                {error && (
                    <div className="mt-2 p-4 bg-gray-700 rounded-lg border border-red-700">
                        <p className="text-red-400">{error}</p>
                    </div>
                )}
                
                <p className="text-xs text-gray-400 mt-6 text-center">
                    Enter a domain name above and click "Resolve" to find its IP address
                </p>
            </div>
        </div>
    );
}

export default App;
