'use client';
import React, { useState } from 'react'
import { fetchOllamaModels } from '@/lib/api-helpers'

const page = () => {
    const [modelDict, setModelDict] = useState<Record<string, string>>({});

    const models = fetchOllamaModels() || {};

    const handleRefresh = async () => {
        const data = await fetchOllamaModels();
        if (data) {
            setModelDict(data); // Now you have your dictionary
            console.log("Dictionary received:", data);
        }
    };
    return (
        <div className="p-6">
            <button
                onClick={handleRefresh}
                className="bg-blue-600 text-white px-4 py-2 rounded"
            >
                Load Models Dictionary
            </button>

            <pre className="mt-4 p-4 bg-gray-100 rounded">
                {JSON.stringify(modelDict, null, 2)}
            </pre>
            
        </div>
    )
}

export default page