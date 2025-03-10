import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFolder, faSort, faSpinner, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';

const FileSorter = () => {
    const [sourceDir, setSourceDir] = useState('');
    const [destDir, setDestDir] = useState('');
    const [criteria, setCriteria] = useState('type');
    const [recursive, setRecursive] = useState(true);
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const sortingCriteria = [
        { value: 'type', label: 'File Type', description: 'Sort files by their type (images, documents, etc.)' },
        { value: 'date', label: 'Date', description: 'Sort files by creation date' },
        { value: 'size', label: 'Size', description: 'Sort files by their size' },
        { value: 'name', label: 'Name', description: 'Sort files alphabetically' }
    ];

    const handleSort = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch('/api/sort-files', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source_dir: sourceDir,
                    dest_dir: destDir,
                    criteria,
                    recursive
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Failed to sort files');
            }

            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const renderStatistics = () => {
        if (!result?.statistics) return null;

        const stats = result.statistics;
        const formatSize = (bytes) => {
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            if (bytes === 0) return '0 Byte';
            const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
            return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
        };

        return (
            <div className="mt-6 bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Sorting Results</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Total Files</p>
                        <p className="text-2xl font-semibold text-gray-900">{stats.total_files}</p>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Total Size</p>
                        <p className="text-2xl font-semibold text-gray-900">{formatSize(stats.total_size)}</p>
                    </div>
                </div>

                <div className="mt-6">
                    <h4 className="text-md font-medium text-gray-900 mb-3">Categories</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {Object.entries(stats.categories).map(([category, data]) => (
                            <div key={category} className="bg-gray-50 rounded-lg p-4">
                                <p className="text-sm font-medium text-gray-900 capitalize">{category}</p>
                                <p className="text-sm text-gray-600">Files: {data.count}</p>
                                <p className="text-sm text-gray-600">Size: {formatSize(data.total_size)}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="px-6 py-4 bg-blue-600 text-white">
                <h2 className="text-xl font-semibold">File Sorter</h2>
                <p className="text-sm text-blue-100">Organize your files automatically based on various criteria</p>
            </div>

            <form onSubmit={handleSort} className="p-6">
                <div className="space-y-6">
                    {/* Source Directory */}
                    <div>
                        <label htmlFor="sourceDir" className="block text-sm font-medium text-gray-700">
                            Source Directory
                        </label>
                        <div className="mt-1 relative rounded-md shadow-sm">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <FontAwesomeIcon icon={faFolder} className="text-gray-400" />
                            </div>
                            <input
                                type="text"
                                id="sourceDir"
                                value={sourceDir}
                                onChange={(e) => setSourceDir(e.target.value)}
                                className="input-field pl-10"
                                placeholder="/path/to/source"
                                required
                            />
                        </div>
                    </div>

                    {/* Destination Directory */}
                    <div>
                        <label htmlFor="destDir" className="block text-sm font-medium text-gray-700">
                            Destination Directory
                        </label>
                        <div className="mt-1 relative rounded-md shadow-sm">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <FontAwesomeIcon icon={faFolder} className="text-gray-400" />
                            </div>
                            <input
                                type="text"
                                id="destDir"
                                value={destDir}
                                onChange={(e) => setDestDir(e.target.value)}
                                className="input-field pl-10"
                                placeholder="/path/to/destination"
                                required
                            />
                        </div>
                    </div>

                    {/* Sorting Criteria */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Sorting Criteria
                        </label>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {sortingCriteria.map(({ value, label, description }) => (
                                <div
                                    key={value}
                                    className={`relative rounded-lg border p-4 cursor-pointer transition-colors ${
                                        criteria === value
                                            ? 'border-blue-500 bg-blue-50'
                                            : 'border-gray-200 hover:border-blue-300'
                                    }`}
                                    onClick={() => setCriteria(value)}
                                >
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <h3 className="text-sm font-medium text-gray-900">{label}</h3>
                                            <p className="text-xs text-gray-500 mt-1">{description}</p>
                                        </div>
                                        {criteria === value && (
                                            <FontAwesomeIcon icon={faCheck} className="text-blue-500" />
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Recursive Option */}
                    <div className="flex items-center">
                        <input
                            type="checkbox"
                            id="recursive"
                            checked={recursive}
                            onChange={(e) => setRecursive(e.target.checked)}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <label htmlFor="recursive" className="ml-2 block text-sm text-gray-900">
                            Include subdirectories
                        </label>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="rounded-md bg-red-50 p-4">
                            <div className="flex">
                                <FontAwesomeIcon icon={faTimes} className="text-red-400" />
                                <div className="ml-3">
                                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                                    <div className="mt-2 text-sm text-red-700">{error}</div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
                            isLoading ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                    >
                        {isLoading ? (
                            <>
                                <FontAwesomeIcon icon={faSpinner} className="animate-spin mr-2" />
                                Sorting Files...
                            </>
                        ) : (
                            <>
                                <FontAwesomeIcon icon={faSort} className="mr-2" />
                                Sort Files
                            </>
                        )}
                    </button>
                </div>
            </form>

            {/* Results */}
            {renderStatistics()}
        </div>
    );
};

export default FileSorter;
